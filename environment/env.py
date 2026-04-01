"""
ContractEnv Phase 2 — Core RL Environment
===========================================

OpenEnv-compliant reinforcement learning environment for legal contract
negotiation.  Implements the canonical ``reset()`` / ``step()`` /
``state()`` API.

The environment operates in three difficulty tiers:

* **task1 (easy)** — Clause identification & flagging only.
* **task2 (medium)** — Clause redlining with proposal quality scoring.
* **task3 (hard)** — Multi-turn negotiation with a deterministic
  counterparty.

All reward signals are dense (per-step) and clamped to [-1.0, 1.0].

Part of the Meta / Scaler OpenEnv Hackathon submission.
"""

from __future__ import annotations

import copy
import logging
from typing import Any, Dict, List, Optional, Set, Tuple

from environment.contracts import load_contract
from environment.counterparty import Counterparty, CounterpartyResponse
from environment.models import (
    Action,
    ActionType,
    Clause,
    ClauseLabel,
    NegotiationTurn,
    Observation,
    Reward,
    RewardBreakdown,
    TaskConfig,
)

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────────────────────────────
# Task configurations (matching openenv.yaml)
# ─────────────────────────────────────────────────────────────────────

TASK_CONFIGS: Dict[str, TaskConfig] = {
    "task1": TaskConfig(
        task_id="task1",
        name="Simple SaaS Agreement",
        difficulty="easy",
        description=(
            "A straightforward NDA with 6 clauses including 4 unfair "
            "terms.  Tests basic clause identification and labelling."
        ),
        max_turns=20,
        target_score=0.85,
    ),
    "task2": TaskConfig(
        task_id="task2",
        name="Enterprise Licensing Deal",
        difficulty="medium",
        description=(
            "An NDA with 4 clauses requiring redlining.  The agent "
            "must propose improved clause language that addresses "
            "unfair terms."
        ),
        max_turns=30,
        target_score=0.65,
    ),
    "task3": TaskConfig(
        task_id="task3",
        name="Cross-Border Partnership Agreement",
        difficulty="hard",
        description=(
            "Full negotiation on 2 deal-breaker clauses with a "
            "deterministic counterparty.  The agent must propose, "
            "respond to counters, and reach agreement."
        ),
        max_turns=40,
        target_score=0.45,
    ),
}


# ─────────────────────────────────────────────────────────────────────
# Reward constants
# ─────────────────────────────────────────────────────────────────────

_R = {
    "flag_correct_unfair":       +0.10,
    "label_correct":             +0.05,
    "proposal_reduce_duration":  +0.10,
    "proposal_narrow_scope":     +0.10,
    "proposal_add_carveout":     +0.08,
    "counterparty_accept":       +0.20,
    "full_agreement":            +0.25,
    "agent_accept_counter":      +0.15,
    "flag_fair_false_positive":  -0.15,
    "break_deal_breaker":        -0.30,
    "exceed_turn_budget":        -0.10,
    "propose_illegal_language":  -0.25,
}

# Keywords that indicate "illegal" / unacceptable proposal language.
_ILLEGAL_KEYWORDS: List[str] = [
    "perpetuity",
    "global",
    "all future",
    "regardless",
    "unlimited",
    "irrevocable",
    "waive all",
    "no limitation",
    "sole discretion",
    "without exception",
]

# Keywords that earn proposal quality bonuses.
_DURATION_KEYWORDS: List[str] = [
    "12 month", "twelve month", "24 month", "one year",
    "two year", "limited period",
]
_SCOPE_KEYWORDS: List[str] = [
    "specific", "narrow", "limited to", "restricted to",
    "defined market", "product categor",
]
_CARVEOUT_KEYWORDS: List[str] = [
    "carve-out", "carve out", "pre-existing", "prior",
    "documented", "schedule", "exclude",
]


# ─────────────────────────────────────────────────────────────────────
# ContractEnv — Main Environment
# ─────────────────────────────────────────────────────────────────────


class ContractEnv:
    """OpenEnv-compliant RL environment for legal contract negotiation.

    Usage::

        env = ContractEnv(task_id="task1")
        obs = env.reset()
        obs, reward, done, info = env.step(action)
        state = env.state()
    """

    def __init__(self, task_id: str = "task1") -> None:
        if task_id not in TASK_CONFIGS:
            raise ValueError(
                f"Unknown task_id '{task_id}'. "
                f"Expected one of: {sorted(TASK_CONFIGS)}"
            )

        self.task_id: str = task_id
        self.task_config: TaskConfig = TASK_CONFIGS[task_id]
        self.counterparty: Counterparty = Counterparty()

        # ── Internal state (populated by reset) ──
        self._contract_data: Dict[str, Any] = {}
        self._clauses: List[Clause] = []
        self._clause_map: Dict[str, Clause] = {}

        self._turn: int = 0
        self._done: bool = True  # Must call reset() first.
        self._negotiation_history: List[NegotiationTurn] = []
        self._current_clause_id: Optional[str] = None

        # Tracking sets
        self._flagged_clauses: Set[str] = set()
        self._proposed_clauses: Set[str] = set()
        self._resolved_clauses: Set[str] = set()
        self._rejected_clauses: Set[str] = set()
        self._skipped_clauses: Set[str] = set()

        # Cumulative score for the episode.
        self._cumulative_score: float = 0.0

        logger.info("ContractEnv initialised for task '%s'.", task_id)

    # ────────────────────────────────────────────────────────────
    # Public API — OpenEnv spec
    # ────────────────────────────────────────────────────────────

    def reset(self) -> Observation:
        """Start a new episode: load a fresh contract and reset state.

        Returns
        -------
        Observation
            The initial observation with full contract text, clauses,
            and zeroed-out progress counters.
        """
        self._contract_data = load_contract(self.task_id)
        self._clauses = list(self._contract_data["clauses"])
        self._clause_map = {c.id: c for c in self._clauses}

        self._turn = 0
        self._done = False
        self._negotiation_history = []

        # Point at the first clause.
        self._current_clause_id = (
            self._clauses[0].id if self._clauses else None
        )

        # Clear tracking sets.
        self._flagged_clauses.clear()
        self._proposed_clauses.clear()
        self._resolved_clauses.clear()
        self._rejected_clauses.clear()
        self._skipped_clauses.clear()

        self._cumulative_score = 0.0

        logger.info("Episode reset for task '%s'.", self.task_id)
        return self._build_observation()

    def step(
        self, action: Action
    ) -> Tuple[Observation, Reward, bool, Dict[str, Any]]:
        """Apply an agent action and advance the environment.

        Parameters
        ----------
        action : Action
            The agent's chosen action for a specific clause.

        Returns
        -------
        tuple[Observation, Reward, bool, dict]
            ``(observation, reward, done, info)``

        Raises
        ------
        RuntimeError
            If called before ``reset()`` or after the episode is done.
        ValueError
            If the action references an unknown clause.
        """
        if self._done:
            raise RuntimeError(
                "Episode is done.  Call reset() to start a new episode."
            )

        # ── Validate ──
        clause = self._clause_map.get(action.clause_id)
        if clause is None:
            raise ValueError(
                f"Unknown clause_id '{action.clause_id}'. "
                f"Valid IDs: {sorted(self._clause_map)}"
            )

        self._turn += 1
        self._current_clause_id = action.clause_id

        # ── Compute reward ──
        reward_value, breakdown = self._compute_reward(action, clause)

        # ── Apply action & maybe get counterparty response ──
        info: Dict[str, Any] = {}
        self._apply_action(action, clause)

        # For task3, run counterparty interaction on propose actions.
        if (
            self.task_id == "task3"
            and action.action_type == ActionType.PROPOSE
            and action.proposed_text
        ):
            cp_response = self._handle_negotiate(action, clause)
            info["counterparty_response"] = cp_response.model_dump()

            # Adjust reward based on counterparty outcome.
            if cp_response.response_type == "accept":
                reward_value += _R["counterparty_accept"]
                breakdown = breakdown.model_copy(
                    update={"agreement_bonus": breakdown.agreement_bonus + _R["counterparty_accept"]}
                )
                self._resolved_clauses.add(action.clause_id)
            elif cp_response.response_type == "deal_breaker_reject":
                reward_value += _R["break_deal_breaker"]
                breakdown = breakdown.model_copy(
                    update={"deal_breaker_penalty": breakdown.deal_breaker_penalty + _R["break_deal_breaker"]}
                )

        # ── Turn-budget penalty ──
        if self._turn > self.task_config.max_turns:
            penalty = _R["exceed_turn_budget"]
            reward_value += penalty
            breakdown = breakdown.model_copy(
                update={"turn_efficiency_penalty": breakdown.turn_efficiency_penalty + penalty}
            )

        # ── Clamp reward ──
        reward_value = max(-1.0, min(1.0, reward_value))
        self._cumulative_score += reward_value

        # ── Check done ──
        self._done = self._check_done()

        # ── Finality bonus ──
        if self._done and len(self._resolved_clauses) == len(self._clauses):
            reward_value = min(1.0, reward_value + _R["full_agreement"])
            breakdown = breakdown.model_copy(
                update={"agreement_bonus": breakdown.agreement_bonus + _R["full_agreement"]}
            )
            # Re-clamp after bonus.
            reward_value = max(-1.0, min(1.0, reward_value))

        # ── Build return objects ──
        reward = Reward(
            value=round(reward_value, 4),
            breakdown=breakdown,
            done=self._done,
            info={
                "turn": self._turn,
                "cumulative_score": round(self._cumulative_score, 4),
                "resolved": len(self._resolved_clauses),
                "remaining": len(self._clauses) - len(self._resolved_clauses),
                **info,
            },
        )

        obs = self._build_observation()
        return obs, reward, self._done, reward.info

    def state(self) -> Dict[str, Any]:
        """Return the full current state (for the ``GET /state`` endpoint).

        Returns
        -------
        dict
            Includes the current observation, episode metadata, and
            internal tracking counters.
        """
        obs = self._build_observation()
        return {
            "observation": obs.model_dump(),
            "task_id": self.task_id,
            "task_config": self.task_config.model_dump(),
            "turn": self._turn,
            "done": self._done,
            "cumulative_score": round(self._cumulative_score, 4),
            "flagged_clauses": sorted(self._flagged_clauses),
            "proposed_clauses": sorted(self._proposed_clauses),
            "resolved_clauses": sorted(self._resolved_clauses),
            "rejected_clauses": sorted(self._rejected_clauses),
            "skipped_clauses": sorted(self._skipped_clauses),
        }

    # ────────────────────────────────────────────────────────────
    # Reward computation
    # ────────────────────────────────────────────────────────────

    def _compute_reward(
        self,
        action: Action,
        clause: Clause,
    ) -> Tuple[float, RewardBreakdown]:
        """Compute the step reward based on action type and clause truth.

        Returns
        -------
        tuple[float, RewardBreakdown]
            Scalar reward (pre-clamp) and its itemised breakdown.
        """
        flag_correct = 0.0
        label_correct = 0.0
        proposal_quality = 0.0
        agreement_bonus = 0.0
        deal_breaker_penalty = 0.0
        false_positive_penalty = 0.0
        turn_efficiency_penalty = 0.0

        gt = clause.ground_truth_label

        # ── FLAG action ──
        if action.action_type == ActionType.FLAG:
            if gt == ClauseLabel.UNFAIR:
                flag_correct = _R["flag_correct_unfair"]
            elif gt in (ClauseLabel.FAIR, ClauseLabel.NEUTRAL):
                false_positive_penalty = _R["flag_fair_false_positive"]

            # Label bonus.
            if action.label and gt and action.label == gt:
                label_correct = _R["label_correct"]

        # ── PROPOSE action ──
        elif action.action_type == ActionType.PROPOSE:
            if action.proposed_text:
                pq = self._score_proposal(action.proposed_text)
                proposal_quality = pq

                # Check for illegal language in proposals.
                if self._has_illegal_language(action.proposed_text):
                    deal_breaker_penalty = _R["propose_illegal_language"]

            # Label bonus.
            if action.label and gt and action.label == gt:
                label_correct = _R["label_correct"]

        # ── ACCEPT action ──
        elif action.action_type == ActionType.ACCEPT:
            if gt == ClauseLabel.UNFAIR and clause.is_deal_breaker:
                # Accepting an unfair deal-breaker is very bad.
                deal_breaker_penalty = _R["break_deal_breaker"]
            elif gt == ClauseLabel.FAIR or gt == ClauseLabel.NEUTRAL:
                # Correctly accepting a fair/neutral clause.
                agreement_bonus = _R["agent_accept_counter"]

        # ── REJECT action ──
        elif action.action_type == ActionType.REJECT:
            if gt == ClauseLabel.UNFAIR:
                flag_correct = _R["flag_correct_unfair"]
            elif gt in (ClauseLabel.FAIR, ClauseLabel.NEUTRAL):
                false_positive_penalty = _R["flag_fair_false_positive"]

        # ── SKIP — no reward or penalty ──

        breakdown = RewardBreakdown(
            flag_correct=round(flag_correct, 4),
            label_correct=round(label_correct, 4),
            proposal_quality=round(proposal_quality, 4),
            agreement_bonus=round(agreement_bonus, 4),
            deal_breaker_penalty=round(deal_breaker_penalty, 4),
            false_positive_penalty=round(false_positive_penalty, 4),
            turn_efficiency_penalty=round(turn_efficiency_penalty, 4),
        )

        total = (
            flag_correct
            + label_correct
            + proposal_quality
            + agreement_bonus
            + deal_breaker_penalty
            + false_positive_penalty
            + turn_efficiency_penalty
        )
        return round(total, 4), breakdown

    # ────────────────────────────────────────────────────────────
    # Proposal quality scoring
    # ────────────────────────────────────────────────────────────

    @staticmethod
    def _score_proposal(proposed_text: str) -> float:
        """Score a proposal based on keyword indicators of quality."""
        text_lower = proposed_text.lower()
        score = 0.0

        # Duration improvement.
        if any(kw in text_lower for kw in _DURATION_KEYWORDS):
            score += _R["proposal_reduce_duration"]

        # Scope narrowing.
        if any(kw in text_lower for kw in _SCOPE_KEYWORDS):
            score += _R["proposal_narrow_scope"]

        # Carve-out / prior-IP protection.
        if any(kw in text_lower for kw in _CARVEOUT_KEYWORDS):
            score += _R["proposal_add_carveout"]

        return round(score, 4)

    @staticmethod
    def _has_illegal_language(proposed_text: str) -> bool:
        """Return True if the proposal contains forbidden language."""
        text_lower = proposed_text.lower()
        return any(kw in text_lower for kw in _ILLEGAL_KEYWORDS)

    # ────────────────────────────────────────────────────────────
    # Action handlers
    # ────────────────────────────────────────────────────────────

    def _apply_action(self, action: Action, clause: Clause) -> None:
        """Update internal tracking state based on the action."""
        content = action.reason or f"Action: {action.action_type.value}"

        if action.action_type == ActionType.FLAG:
            self._handle_flag(action, clause)
        elif action.action_type == ActionType.PROPOSE:
            self._handle_propose(action, clause)
        elif action.action_type == ActionType.ACCEPT:
            self._resolved_clauses.add(action.clause_id)
            content = action.reason or "Accepted clause as-is."
        elif action.action_type == ActionType.REJECT:
            self._rejected_clauses.add(action.clause_id)
            self._resolved_clauses.add(action.clause_id)
            content = action.reason or "Rejected clause."
        elif action.action_type == ActionType.SKIP:
            self._skipped_clauses.add(action.clause_id)
            content = action.reason or "Skipped clause."

        # Record the agent's turn.
        self._negotiation_history.append(
            NegotiationTurn(
                turn_number=self._turn,
                speaker="agent",
                action_type=action.action_type,
                clause_id=action.clause_id,
                content=content,
            )
        )

    def _handle_flag(self, action: Action, clause: Clause) -> None:
        """Handle a FLAG action — mark clause as flagged."""
        self._flagged_clauses.add(action.clause_id)
        # For task1/task2, flagging also resolves the clause.
        if self.task_id in ("task1", "task2"):
            self._resolved_clauses.add(action.clause_id)

    def _handle_propose(self, action: Action, clause: Clause) -> None:
        """Handle a PROPOSE action — record the redline proposal."""
        self._proposed_clauses.add(action.clause_id)
        # For task2, proposing resolves the clause (no counterparty).
        if self.task_id == "task2":
            self._resolved_clauses.add(action.clause_id)

    def _handle_negotiate(
        self,
        action: Action,
        clause: Clause,
    ) -> CounterpartyResponse:
        """Handle counterparty interaction for task3 negotiations.

        Returns
        -------
        CounterpartyResponse
            The counterparty's deterministic response.
        """
        proposed_text = action.proposed_text or ""
        cp_response = self.counterparty.respond(
            clause=clause,
            proposed_text=proposed_text,
            turn=self._turn,
        )

        # Record the counterparty turn.
        self._negotiation_history.append(
            NegotiationTurn(
                turn_number=self._turn,
                speaker="counterparty",
                action_type=(
                    ActionType.ACCEPT
                    if cp_response.response_type == "accept"
                    else ActionType.PROPOSE
                    if cp_response.response_type == "counter"
                    else ActionType.REJECT
                ),
                clause_id=action.clause_id,
                content=cp_response.message,
            )
        )

        return cp_response

    # ────────────────────────────────────────────────────────────
    # State helpers
    # ────────────────────────────────────────────────────────────

    def _check_done(self) -> bool:
        """Check whether the episode should end."""
        # All clauses resolved.
        if len(self._resolved_clauses) >= len(self._clauses):
            return True
        # Turn budget exhausted (with a small grace buffer).
        if self._turn >= self.task_config.max_turns + 5:
            return True
        return False

    def _build_observation(self) -> Observation:
        """Construct the current observation.

        Ground-truth labels are stripped from clauses so the agent
        cannot cheat.
        """
        # Deep-copy clauses and hide ground-truth labels.
        visible_clauses = []
        for c in self._clauses:
            visible = c.model_copy(update={"ground_truth_label": None})
            visible_clauses.append(visible)

        return Observation(
            contract_id=self._contract_data.get(
                "contract_id", "unknown"
            ),
            contract_title=self._contract_data.get(
                "contract_title", "Unknown Contract"
            ),
            contract_text=self._contract_data.get(
                "contract_text", ""
            ),
            clauses=visible_clauses,
            negotiation_history=list(self._negotiation_history),
            current_clause_id=self._current_clause_id,
            turn=self._turn,
            max_turns=self.task_config.max_turns,
            task_id=self.task_id,
            agreements_reached=len(self._resolved_clauses),
            total_clauses=len(self._clauses),
        )
