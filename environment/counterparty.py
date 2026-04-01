"""
ContractEnv Phase 2 — Deterministic Counterparty Engine
========================================================

A scripted, keyword-based state machine that simulates a counterparty
during clause-level negotiation.  Responses are fully deterministic so
that grading is reproducible — no LLM calls, no randomness.

The counterparty evaluates the agent's proposed text against a set of
keyword rules per clause category and responds with one of:

* **accept**  — The proposal meets the threshold for agreement.
* **counter** — The proposal is reasonable but needs modification.
* **reject**  — The proposal contains unacceptable language.
* **deal_breaker_reject** — The proposal violates a red-line term.

Part of the Meta / Scaler OpenEnv Hackathon submission.
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

from environment.models import Clause, ClauseCategory


# ─────────────────────────────────────────────────────────────────────
# Response model
# ─────────────────────────────────────────────────────────────────────


class CounterpartyResponse(BaseModel):
    """Structured response returned by the counterparty state machine."""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "response_type": "accept",
                    "message": "We find the revised scope acceptable.",
                    "modified_text": None,
                    "score_impact": 0.20,
                },
                {
                    "response_type": "counter",
                    "message": "We can consider a shorter duration but need specifics.",
                    "modified_text": (
                        "The non-compete period shall be limited to 12 months "
                        "within the specific geographic markets where the "
                        "Disclosing Party actively operates."
                    ),
                    "score_impact": 0.05,
                },
            ]
        }
    )

    response_type: Literal["accept", "counter", "reject", "deal_breaker_reject"] = Field(
        ...,
        description="Type of counterparty response.",
    )
    message: str = Field(
        ...,
        description="Human-readable message explaining the counterparty's stance.",
    )
    modified_text: Optional[str] = Field(
        default=None,
        description="Counter-proposed clause text (only for 'counter' responses).",
    )
    score_impact: float = Field(
        default=0.0,
        description="Reward impact this response has on the agent's score.",
    )


# ─────────────────────────────────────────────────────────────────────
# Keyword rule sets (lowercased for matching)
# ─────────────────────────────────────────────────────────────────────

# Keywords that trigger an ACCEPT response — agent's proposal is strong.
_ACCEPT_KEYWORDS: List[str] = [
    "specific",
    "schedule",
    "12 month",
    "twelve month",
    "carve-out",
    "carve out",
    "prior",
    "documented",
    "pre-existing",
    "reasonable scope",
    "limited to",
    "mutual",
]

# Keywords that trigger a COUNTER response — proposal is on the right
# track but needs refinement.
_COUNTER_KEYWORDS: List[str] = [
    "year",
    "narrow",
    "limit",
    "reasonable",
    "reduce",
    "modify",
    "amend",
    "shorter",
    "restricted",
    "clarify",
]

# Keywords that trigger a hard REJECT — proposal contains unacceptable
# language or over-reaches.
_REJECT_KEYWORDS: List[str] = [
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


# ─────────────────────────────────────────────────────────────────────
# Pre-written counter-offers per clause category
# ─────────────────────────────────────────────────────────────────────

_COUNTER_OFFERS: Dict[ClauseCategory, str] = {
    ClauseCategory.SCOPE: (
        "We can consider narrowing the non-compete to a 12-month period "
        "limited to the specific product categories where the Disclosing "
        "Party actively operates, with a documented list of restricted "
        "activities provided as a schedule to this Agreement."
    ),
    ClauseCategory.IP: (
        "We propose limiting the IP assignment to work product created "
        "exclusively in performance of this Agreement. Pre-existing "
        "intellectual property and independently developed inventions "
        "shall remain with the originating party, documented via a "
        "prior-IP schedule."
    ),
    ClauseCategory.DURATION: (
        "We suggest a confidentiality period of 24 months from disclosure, "
        "with automatic expiry for information that becomes publicly "
        "available through no fault of the Receiving Party."
    ),
    ClauseCategory.LIABILITY: (
        "We propose capping aggregate liability at the greater of (a) the "
        "fees paid under this Agreement in the preceding 12 months, or "
        "(b) $500,000. Injunctive relief should require a showing of "
        "irreparable harm and a court order."
    ),
    ClauseCategory.JURISDICTION: (
        "We propose submitting disputes to binding arbitration under the "
        "rules of the American Arbitration Association, seated in "
        "Wilmington, Delaware."
    ),
    ClauseCategory.PAYMENT: (
        "We suggest Net-30 payment terms with a documented schedule of "
        "milestones and deliverables tied to each payment tranche."
    ),
    ClauseCategory.TERMINATION: (
        "Either party may terminate for material breach upon 30 days' "
        "written notice, with a 15-day cure period. Termination for "
        "convenience requires 60 days' notice."
    ),
}


# ─────────────────────────────────────────────────────────────────────
# Per-clause scripted response tables
# ─────────────────────────────────────────────────────────────────────

_SCRIPTED_RESPONSES: Dict[str, Dict[str, CounterpartyResponse]] = {
    # ── Non-Compete (c2) ──
    "c2": {
        "accept": CounterpartyResponse(
            response_type="accept",
            message=(
                "We agree to the proposed non-compete terms. The 12-month "
                "period limited to specific markets is acceptable."
            ),
            modified_text=None,
            score_impact=0.20,
        ),
        "counter": CounterpartyResponse(
            response_type="counter",
            message=(
                "We appreciate the effort to narrow the scope. However, "
                "we need the restricted period to cover at least the "
                "specific product lines we discussed. Here is our "
                "counter-proposal."
            ),
            modified_text=_COUNTER_OFFERS[ClauseCategory.SCOPE],
            score_impact=0.05,
        ),
        "reject": CounterpartyResponse(
            response_type="reject",
            message=(
                "We cannot agree to a non-compete that applies on a "
                "global basis in perpetuity. Please revise with "
                "reasonable geographic and temporal limitations."
            ),
            modified_text=None,
            score_impact=-0.10,
        ),
        "deal_breaker_reject": CounterpartyResponse(
            response_type="deal_breaker_reject",
            message=(
                "This proposal would effectively prevent any future "
                "business activity. We consider this a deal-breaker and "
                "must reject it outright."
            ),
            modified_text=None,
            score_impact=-0.30,
        ),
    },
    # ── IP Assignment (c3) ──
    "c3": {
        "accept": CounterpartyResponse(
            response_type="accept",
            message=(
                "We accept the revised IP assignment clause. Limiting "
                "assignment to work product created for this engagement, "
                "with a prior-IP schedule, is reasonable."
            ),
            modified_text=None,
            score_impact=0.20,
        ),
        "counter": CounterpartyResponse(
            response_type="counter",
            message=(
                "We can consider limiting the scope, but we need "
                "clearer definitions of 'pre-existing IP'. Here is "
                "our counter-proposal."
            ),
            modified_text=_COUNTER_OFFERS[ClauseCategory.IP],
            score_impact=0.05,
        ),
        "reject": CounterpartyResponse(
            response_type="reject",
            message=(
                "We cannot accept an IP clause that claims ownership "
                "regardless of prior development. This must be revised."
            ),
            modified_text=None,
            score_impact=-0.10,
        ),
        "deal_breaker_reject": CounterpartyResponse(
            response_type="deal_breaker_reject",
            message=(
                "Claiming all IP irrevocably, including pre-existing "
                "work, is a fundamental deal-breaker. We reject this."
            ),
            modified_text=None,
            score_impact=-0.30,
        ),
    },
    # ── Confidentiality Scope (c1) ──
    "c1": {
        "accept": CounterpartyResponse(
            response_type="accept",
            message=(
                "The proposed confidentiality scope with specific "
                "categories and a time limit is acceptable."
            ),
            modified_text=None,
            score_impact=0.20,
        ),
        "counter": CounterpartyResponse(
            response_type="counter",
            message=(
                "We agree confidentiality should not be perpetual, but "
                "we need at least a 24-month period. Here is our "
                "counter-proposal."
            ),
            modified_text=_COUNTER_OFFERS[ClauseCategory.DURATION],
            score_impact=0.05,
        ),
        "reject": CounterpartyResponse(
            response_type="reject",
            message=(
                "We cannot narrow the confidentiality scope this "
                "drastically. Please provide a more balanced revision."
            ),
            modified_text=None,
            score_impact=-0.10,
        ),
    },
    # ── Remedies / Liability (c6) ──
    "c6": {
        "accept": CounterpartyResponse(
            response_type="accept",
            message=(
                "The proposed liability cap and injunctive relief "
                "requirements are reasonable. We accept."
            ),
            modified_text=None,
            score_impact=0.20,
        ),
        "counter": CounterpartyResponse(
            response_type="counter",
            message=(
                "We need injunctive relief to remain available, but can "
                "agree to a liability cap. Here is our counter-proposal."
            ),
            modified_text=_COUNTER_OFFERS[ClauseCategory.LIABILITY],
            score_impact=0.05,
        ),
        "reject": CounterpartyResponse(
            response_type="reject",
            message=(
                "Removing all remedies is not acceptable. We need at "
                "least injunctive relief for material breaches."
            ),
            modified_text=None,
            score_impact=-0.10,
        ),
    },
}


# ─────────────────────────────────────────────────────────────────────
# Counterparty state machine
# ─────────────────────────────────────────────────────────────────────


class Counterparty:
    """Deterministic, keyword-based counterparty for contract negotiation.

    Evaluates the agent's proposed clause text against keyword rule sets
    and returns a scripted :class:`CounterpartyResponse`.  No randomness,
    no LLM calls — fully reproducible for automated grading.
    """

    def respond(
        self,
        clause: Clause,
        proposed_text: str,
        turn: int,
    ) -> CounterpartyResponse:
        """Evaluate a proposal and return a deterministic response.

        Parameters
        ----------
        clause : Clause
            The clause being negotiated.
        proposed_text : str
            The agent's proposed replacement text.
        turn : int
            Current negotiation turn (used for tie-breaking).

        Returns
        -------
        CounterpartyResponse
        """
        text_lower = proposed_text.lower()

        # 1. Check for deal-breaker violations first.
        if clause.is_deal_breaker and self._has_reject_keywords(text_lower):
            return self._get_scripted("deal_breaker_reject", clause)

        # 2. Check for hard-reject keywords.
        if self._has_reject_keywords(text_lower):
            return self._get_scripted("reject", clause)

        # 3. Check for accept keywords (proposal is strong).
        accept_count = self._count_keywords(text_lower, _ACCEPT_KEYWORDS)
        counter_count = self._count_keywords(text_lower, _COUNTER_KEYWORDS)

        if accept_count >= 2:
            return self._get_scripted("accept", clause)

        # 4. Check for counter keywords (proposal is on the right track).
        if counter_count >= 1 or accept_count == 1:
            return self._get_scripted("counter", clause)

        # 5. Fallback: if no keywords match, counter with guidance.
        return self._get_scripted("counter", clause)

    def get_counter_offer(self, clause: Clause) -> str:
        """Return a pre-written counter-offer for the given clause.

        Parameters
        ----------
        clause : Clause
            The clause to generate a counter-offer for.

        Returns
        -------
        str
            Pre-written counter-offer text.
        """
        return _COUNTER_OFFERS.get(
            clause.category,
            (
                "We suggest revising this clause with more specific "
                "terms and reasonable limitations that protect both "
                "parties' interests."
            ),
        )

    # ── Private helpers ──────────────────────────────────────────────

    @staticmethod
    def _has_reject_keywords(text_lower: str) -> bool:
        """Return True if the text contains any hard-reject keyword."""
        return any(kw in text_lower for kw in _REJECT_KEYWORDS)

    @staticmethod
    def _count_keywords(text_lower: str, keywords: List[str]) -> int:
        """Count how many keywords from *keywords* appear in the text."""
        return sum(1 for kw in keywords if kw in text_lower)

    @staticmethod
    def _get_scripted(
        response_key: str,
        clause: Clause,
    ) -> CounterpartyResponse:
        """Look up a scripted response for a clause, with fallback."""
        clause_responses = _SCRIPTED_RESPONSES.get(clause.id)
        if clause_responses and response_key in clause_responses:
            return clause_responses[response_key]

        # Fallback for clauses without scripted entries.
        fallback_messages: Dict[str, CounterpartyResponse] = {
            "accept": CounterpartyResponse(
                response_type="accept",
                message="We find the revised terms acceptable.",
                score_impact=0.20,
            ),
            "counter": CounterpartyResponse(
                response_type="counter",
                message=(
                    "We appreciate the proposal but need further "
                    "refinement. Please provide more specific terms."
                ),
                modified_text=_COUNTER_OFFERS.get(
                    clause.category,
                    "Please revise with specific, reasonable limitations.",
                ),
                score_impact=0.05,
            ),
            "reject": CounterpartyResponse(
                response_type="reject",
                message=(
                    "We cannot accept this proposal as written. "
                    "Please remove overly broad or unreasonable language."
                ),
                score_impact=-0.10,
            ),
            "deal_breaker_reject": CounterpartyResponse(
                response_type="deal_breaker_reject",
                message=(
                    "This proposal violates a fundamental term. "
                    "We must reject it as a deal-breaker."
                ),
                score_impact=-0.30,
            ),
        }
        return fallback_messages[response_key]
