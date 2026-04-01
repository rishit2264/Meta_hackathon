"""
ContractEnv Phase 1 — Pydantic v2 Data Models
===============================================

Core data models for the ContractEnv reinforcement learning environment.
ContractEnv is an OpenEnv-compliant environment where an AI agent negotiates
legal business contracts clause by clause, identifying unfair terms, proposing
redlines, and reaching agreements with a simulated counterparty.

These models define the observation space, action space, reward structure,
and all intermediate data types used throughout the environment.

Part of the Meta/Scaler OpenEnv Hackathon submission.
"""

from __future__ import annotations

from enum import Enum
from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


# ─────────────────────────────────────────────────────────────────────
# Enums
# ─────────────────────────────────────────────────────────────────────


class ClauseCategory(str, Enum):
    """Categories of contract clauses that the agent must analyse.

    Each category represents a common section found in business contracts.
    The agent should apply category-specific heuristics when evaluating
    fairness and proposing redlines.
    """

    SCOPE = "scope"
    DURATION = "duration"
    IP = "ip"
    LIABILITY = "liability"
    JURISDICTION = "jurisdiction"
    PAYMENT = "payment"
    TERMINATION = "termination"


class ClauseLabel(str, Enum):
    """Fairness label assigned to a contract clause.

    The agent's primary classification task is to label each clause
    as fair, unfair, or neutral based on industry norms and the
    interests of the reviewing party.
    """

    FAIR = "fair"
    UNFAIR = "unfair"
    NEUTRAL = "neutral"


class ActionType(str, Enum):
    """Discrete actions available to the negotiating agent.

    * **flag**    – Mark a clause for further review.
    * **propose** – Suggest alternative contract language.
    * **accept**  – Accept the clause as-is.
    * **reject**  – Reject the clause outright.
    * **skip**    – Skip the clause without taking any stance.
    """

    FLAG = "flag"
    PROPOSE = "propose"
    ACCEPT = "accept"
    REJECT = "reject"
    SKIP = "skip"


class CounterpartyState(str, Enum):
    """State of the simulated counterparty for a given clause.

    Tracks the counterparty's stance during multi-turn negotiation
    on a single clause.
    """

    PENDING = "pending"
    COUNTERED = "countered"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


# ─────────────────────────────────────────────────────────────────────
# Core Data Models
# ─────────────────────────────────────────────────────────────────────


class Clause(BaseModel):
    """Represents a single clause within a contract.

    Each clause carries its raw text, a categorical tag, and an optional
    ground-truth label used during evaluation / reward computation.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "id": "clause-001",
                    "title": "Limitation of Liability",
                    "text": (
                        "The Provider's total aggregate liability under this "
                        "Agreement shall not exceed the fees paid by the Client "
                        "in the 12 months preceding the claim."
                    ),
                    "category": "liability",
                    "is_deal_breaker": False,
                    "ground_truth_label": "fair",
                },
                {
                    "id": "clause-002",
                    "title": "Intellectual Property Assignment",
                    "text": (
                        "All work product, inventions, and intellectual property "
                        "created by the Client during the term of this Agreement "
                        "shall be the sole and exclusive property of the Provider, "
                        "including any pre-existing IP contributed by the Client."
                    ),
                    "category": "ip",
                    "is_deal_breaker": True,
                    "ground_truth_label": "unfair",
                },
            ]
        }
    )

    id: str = Field(
        ...,
        description="Unique identifier for the clause (e.g. 'clause-001').",
    )
    title: str = Field(
        ...,
        description="Short human-readable title summarising the clause.",
    )
    text: str = Field(
        ...,
        description="Full verbatim text of the contract clause.",
    )
    category: ClauseCategory = Field(
        ...,
        description="High-level category this clause belongs to.",
    )
    is_deal_breaker: bool = Field(
        default=False,
        description=(
            "If True, incorrectly handling this clause incurs a large "
            "penalty. Deal-breaker clauses represent critical business risks."
        ),
    )
    ground_truth_label: Optional[ClauseLabel] = Field(
        default=None,
        description=(
            "Expert-annotated fairness label. Used for reward computation "
            "but hidden from the agent during inference."
        ),
    )


class NegotiationTurn(BaseModel):
    """A single turn in the negotiation dialogue between agent and counterparty.

    Turns are appended to the negotiation history and exposed in the
    observation so the agent can condition on prior exchanges.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "turn_number": 1,
                    "speaker": "agent",
                    "action_type": "flag",
                    "clause_id": "clause-002",
                    "content": (
                        "This IP assignment clause is overly broad. It claims "
                        "ownership of the Client's pre-existing IP, which is "
                        "non-standard and unfair."
                    ),
                    "reward_delta": 0.15,
                },
                {
                    "turn_number": 2,
                    "speaker": "counterparty",
                    "action_type": "propose",
                    "clause_id": "clause-002",
                    "content": (
                        "We can narrow the scope to work product created "
                        "solely for this engagement, excluding pre-existing IP."
                    ),
                    "reward_delta": 0.0,
                },
            ]
        }
    )

    turn_number: int = Field(
        ...,
        description="Sequential 1-based index of this turn in the negotiation.",
    )
    speaker: Literal["agent", "counterparty"] = Field(
        ...,
        description="Who produced this turn — the RL agent or the simulated counterparty.",
    )
    action_type: ActionType = Field(
        ...,
        description="The type of action taken during this turn.",
    )
    clause_id: str = Field(
        ...,
        description="ID of the clause this turn pertains to.",
    )
    content: str = Field(
        ...,
        description=(
            "Free-text content of the turn — reasoning, proposed redline, "
            "or counterparty response."
        ),
    )
    reward_delta: float = Field(
        default=0.0,
        description=(
            "Incremental reward earned or lost on this turn. "
            "Only non-zero for agent turns."
        ),
    )


class Observation(BaseModel):
    """The full observation returned to the agent at each step.

    Contains everything the agent needs to decide its next action:
    the contract text, clause list, negotiation history, and progress
    metadata.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "contract_id": "contract-saas-001",
                    "contract_title": "SaaS Service Agreement — Acme Corp",
                    "contract_text": (
                        "This Software-as-a-Service Agreement is entered into "
                        "between Acme Corp ('Provider') and Beta Inc ('Client')..."
                    ),
                    "clauses": [
                        {
                            "id": "clause-001",
                            "title": "Limitation of Liability",
                            "text": (
                                "The Provider's total aggregate liability shall "
                                "not exceed the fees paid in the preceding 12 months."
                            ),
                            "category": "liability",
                            "is_deal_breaker": False,
                            "ground_truth_label": None,
                        }
                    ],
                    "negotiation_history": [],
                    "current_clause_id": "clause-001",
                    "turn": 0,
                    "max_turns": 20,
                    "task_id": "task1",
                    "agreements_reached": 0,
                    "total_clauses": 5,
                }
            ]
        }
    )

    contract_id: str = Field(
        ...,
        description="Unique identifier for the contract being negotiated.",
    )
    contract_title: str = Field(
        ...,
        description="Human-readable title of the contract.",
    )
    contract_text: str = Field(
        ...,
        description="Full raw text of the contract document.",
    )
    clauses: List[Clause] = Field(
        ...,
        description="Ordered list of clauses extracted from the contract.",
    )
    negotiation_history: List[NegotiationTurn] = Field(
        default_factory=list,
        description="Chronological list of all negotiation turns so far.",
    )
    current_clause_id: Optional[str] = Field(
        default=None,
        description="ID of the clause currently under negotiation, if any.",
    )
    turn: int = Field(
        ...,
        description="Current turn number (0-indexed).",
    )
    max_turns: int = Field(
        ...,
        description="Maximum number of turns allowed for this episode.",
    )
    task_id: str = Field(
        ...,
        description="Identifier of the active task configuration.",
    )
    agreements_reached: int = Field(
        default=0,
        description="Number of clauses successfully resolved so far.",
    )
    total_clauses: int = Field(
        ...,
        description="Total number of clauses in the contract.",
    )


class Action(BaseModel):
    """An action submitted by the agent to the environment.

    Encapsulates the agent's decision for a specific clause: which
    action to take, an optional fairness label, reasoning, and (for
    proposals) suggested replacement text.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "clause_id": "clause-002",
                    "action_type": "propose",
                    "label": "unfair",
                    "reason": (
                        "The IP assignment is overly broad. It should be "
                        "narrowed to work product created solely for this "
                        "engagement."
                    ),
                    "proposed_text": (
                        "All work product created by the Client exclusively "
                        "in performance of this Agreement shall be assigned "
                        "to the Provider. Pre-existing IP remains with the "
                        "originating party."
                    ),
                },
                {
                    "clause_id": "clause-001",
                    "action_type": "accept",
                    "label": "fair",
                    "reason": (
                        "The liability cap is reasonable and aligns with "
                        "industry standards for SaaS agreements."
                    ),
                    "proposed_text": None,
                },
            ]
        }
    )

    clause_id: str = Field(
        ...,
        description="ID of the clause this action targets.",
    )
    action_type: ActionType = Field(
        ...,
        description="The type of action the agent is taking.",
    )
    label: Optional[ClauseLabel] = Field(
        default=None,
        description=(
            "Optional fairness label the agent assigns to the clause. "
            "Required when action_type is 'flag'."
        ),
    )
    reason: Optional[str] = Field(
        default=None,
        description=(
            "Free-text explanation of why the agent chose this action. "
            "Used for interpretability and partial-credit scoring."
        ),
    )
    proposed_text: Optional[str] = Field(
        default=None,
        description=(
            "Replacement clause text proposed by the agent. "
            "Only meaningful when action_type is 'propose'."
        ),
    )


class RewardBreakdown(BaseModel):
    """Itemised breakdown of the reward signal for a single step.

    Each component captures a distinct aspect of negotiation quality,
    enabling fine-grained analysis and reward shaping.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "flag_correct": 0.20,
                    "label_correct": 0.15,
                    "proposal_quality": 0.30,
                    "agreement_bonus": 0.10,
                    "deal_breaker_penalty": 0.00,
                    "false_positive_penalty": 0.00,
                    "turn_efficiency_penalty": -0.05,
                }
            ]
        }
    )

    flag_correct: float = Field(
        default=0.0,
        description=(
            "Reward for correctly flagging an unfair clause "
            "(or correctly not flagging a fair one)."
        ),
    )
    label_correct: float = Field(
        default=0.0,
        description=(
            "Reward for assigning the correct fairness label "
            "(fair / unfair / neutral)."
        ),
    )
    proposal_quality: float = Field(
        default=0.0,
        description=(
            "Reward based on the semantic quality of a proposed "
            "redline relative to the ground-truth improvement."
        ),
    )
    agreement_bonus: float = Field(
        default=0.0,
        description=(
            "Bonus awarded when the agent and counterparty reach "
            "an agreement on a clause."
        ),
    )
    deal_breaker_penalty: float = Field(
        default=0.0,
        description=(
            "Penalty incurred for mishandling a deal-breaker clause "
            "(e.g. accepting an unfair deal-breaker)."
        ),
    )
    false_positive_penalty: float = Field(
        default=0.0,
        description=(
            "Penalty for incorrectly flagging a fair clause as unfair, "
            "wasting negotiation capital."
        ),
    )
    turn_efficiency_penalty: float = Field(
        default=0.0,
        description=(
            "Small penalty applied each turn to incentivise efficient "
            "negotiation and discourage stalling."
        ),
    )


class Reward(BaseModel):
    """Reward returned by the environment after each agent step.

    Wraps a scalar reward value with a detailed breakdown, a done
    flag, and an extensible info dict for debugging / logging.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "value": 0.70,
                    "breakdown": {
                        "flag_correct": 0.20,
                        "label_correct": 0.15,
                        "proposal_quality": 0.30,
                        "agreement_bonus": 0.10,
                        "deal_breaker_penalty": 0.00,
                        "false_positive_penalty": 0.00,
                        "turn_efficiency_penalty": -0.05,
                    },
                    "done": False,
                    "info": {
                        "clauses_remaining": 4,
                        "current_clause": "clause-002",
                    },
                }
            ]
        }
    )

    value: float = Field(
        ...,
        description=(
            "Scalar reward value for this step, clamped to [-1.0, 1.0]. "
            "Positive values indicate good negotiation moves."
        ),
    )
    breakdown: RewardBreakdown = Field(
        ...,
        description="Itemised breakdown of reward components.",
    )
    done: bool = Field(
        ...,
        description=(
            "True when the episode has ended — either all clauses are "
            "resolved or the turn limit has been reached."
        ),
    )
    info: Dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Auxiliary information for debugging, logging, or "
            "curriculum-learning controllers."
        ),
    )


class TaskConfig(BaseModel):
    """Configuration for a single evaluation task.

    Tasks define difficulty tiers and target scores, aligning with
    the OpenEnv specification's task-based evaluation protocol.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "task_id": "task1",
                    "name": "Simple SaaS Agreement",
                    "difficulty": "easy",
                    "description": (
                        "A straightforward SaaS agreement with 5 clauses, "
                        "including 2 clearly unfair terms. Ideal for testing "
                        "basic clause identification capabilities."
                    ),
                    "max_turns": 20,
                    "target_score": 0.85,
                },
                {
                    "task_id": "task2",
                    "name": "Enterprise Licensing Deal",
                    "difficulty": "medium",
                    "description": (
                        "A multi-section enterprise licence agreement with "
                        "8 clauses. Contains subtle unfairness in IP and "
                        "liability sections requiring nuanced analysis."
                    ),
                    "max_turns": 30,
                    "target_score": 0.65,
                },
                {
                    "task_id": "task3",
                    "name": "Cross-Border Partnership Agreement",
                    "difficulty": "hard",
                    "description": (
                        "A complex international partnership contract with "
                        "12 clauses spanning multiple jurisdictions. Features "
                        "ambiguous language, nested deal-breakers, and an "
                        "aggressive counterparty."
                    ),
                    "max_turns": 40,
                    "target_score": 0.45,
                },
            ]
        }
    )

    task_id: str = Field(
        ...,
        description="Unique task identifier referenced by the OpenEnv spec.",
    )
    name: str = Field(
        ...,
        description="Human-readable task name.",
    )
    difficulty: Literal["easy", "medium", "hard"] = Field(
        ...,
        description="Difficulty tier for curriculum-based evaluation.",
    )
    description: str = Field(
        ...,
        description="Detailed description of what the task involves.",
    )
    max_turns: int = Field(
        ...,
        description="Maximum negotiation turns allowed for this task.",
    )
    target_score: float = Field(
        ...,
        description=(
            "Minimum normalised score (0.0–1.0) the agent should achieve "
            "to be considered successful on this task."
        ),
    )
