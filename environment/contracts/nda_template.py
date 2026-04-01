"""
ContractEnv Phase 2 — NDA Contract Template
=============================================

Hardcoded NDA contract with 6 clauses, each carrying a ground-truth
fairness label used for deterministic reward computation during grading.

The template is shared across all three difficulty tiers; the
``load_nda_contract`` function selects the relevant clause subset and
metadata for each task.

Part of the Meta / Scaler OpenEnv Hackathon submission.
"""

from __future__ import annotations

from typing import Any, Dict, List

from environment.models import Clause, ClauseCategory, ClauseLabel


# ─────────────────────────────────────────────────────────────────────
# Contract identity
# ─────────────────────────────────────────────────────────────────────

NDA_TITLE = "Non-Disclosure Agreement — Acquirer Corp / Startup Inc"

NDA_METADATA: Dict[str, Any] = {
    "contract_id": "nda-acquirer-startup-001",
    "parties": ["Acquirer Corp", "Startup Inc"],
    "date": "2024-06-15",
    "jurisdiction": "Delaware, USA",
}


# ─────────────────────────────────────────────────────────────────────
# Clause definitions (ground-truth labels included)
# ─────────────────────────────────────────────────────────────────────

NDA_CLAUSES: List[Clause] = [
    # ── c1: Confidentiality Scope — UNFAIR ──
    Clause(
        id="c1",
        title="Confidentiality Scope",
        category=ClauseCategory.IP,
        is_deal_breaker=False,
        ground_truth_label=ClauseLabel.UNFAIR,
        text=(
            "All information disclosed by the Disclosing Party to the "
            "Receiving Party, whether oral, written, electronic, or visual, "
            "shall be deemed confidential and proprietary information "
            "('Confidential Information') in perpetuity. This includes, "
            "without limitation, all business plans, financial data, "
            "customer lists, technical specifications, trade secrets, "
            "and any information that would reasonably be considered "
            "confidential, regardless of whether it is explicitly marked "
            "as such. The Receiving Party shall have no right to challenge "
            "the confidential nature of any disclosed information."
        ),
    ),
    # ── c2: Non-Compete — UNFAIR (deal-breaker) ──
    Clause(
        id="c2",
        title="Non-Compete Obligation",
        category=ClauseCategory.SCOPE,
        is_deal_breaker=True,
        ground_truth_label=ClauseLabel.UNFAIR,
        text=(
            "The Receiving Party agrees not to engage, directly or "
            "indirectly, in any business activity that competes with the "
            "Disclosing Party's current or future products, services, or "
            "lines of business for a period of five (5) years following "
            "the termination of this Agreement, on a global basis. This "
            "restriction applies to any capacity, including as an owner, "
            "partner, shareholder, consultant, agent, employee, or in any "
            "other capacity whatsoever, without the prior written consent "
            "of the Disclosing Party."
        ),
    ),
    # ── c3: IP Assignment — UNFAIR (deal-breaker) ──
    Clause(
        id="c3",
        title="Intellectual Property Assignment",
        category=ClauseCategory.IP,
        is_deal_breaker=True,
        ground_truth_label=ClauseLabel.UNFAIR,
        text=(
            "Any and all ideas, inventions, discoveries, concepts, "
            "improvements, works of authorship, and other intellectual "
            "property conceived, created, or developed by the Receiving "
            "Party during the term of this Agreement or within twelve (12) "
            "months following its termination, whether or not related to "
            "the Disclosing Party's business, shall be the sole and "
            "exclusive property of the Disclosing Party and are hereby "
            "irrevocably assigned to the Disclosing Party, regardless of "
            "prior ownership or independent development by the Receiving "
            "Party."
        ),
    ),
    # ── c4: Governing Law — NEUTRAL ──
    Clause(
        id="c4",
        title="Governing Law and Jurisdiction",
        category=ClauseCategory.JURISDICTION,
        is_deal_breaker=False,
        ground_truth_label=ClauseLabel.NEUTRAL,
        text=(
            "This Agreement shall be governed by and construed in "
            "accordance with the laws of the State of Delaware, United "
            "States of America, without regard to its conflict of law "
            "provisions. Any dispute arising out of or in connection with "
            "this Agreement shall be subject to the exclusive jurisdiction "
            "of the state and federal courts located in Wilmington, "
            "Delaware."
        ),
    ),
    # ── c5: Term / Duration — FAIR ──
    Clause(
        id="c5",
        title="Term and Duration",
        category=ClauseCategory.DURATION,
        is_deal_breaker=False,
        ground_truth_label=ClauseLabel.FAIR,
        text=(
            "This Agreement shall remain in effect for a period of two "
            "(2) years from the date of signing. Either party may "
            "terminate this Agreement at any time upon thirty (30) days' "
            "prior written notice to the other party. Upon termination, "
            "the Receiving Party shall promptly return or destroy all "
            "Confidential Information in its possession."
        ),
    ),
    # ── c6: Remedies / Liability — UNFAIR ──
    Clause(
        id="c6",
        title="Remedies and Liability",
        category=ClauseCategory.LIABILITY,
        is_deal_breaker=False,
        ground_truth_label=ClauseLabel.UNFAIR,
        text=(
            "The Receiving Party acknowledges that any breach of this "
            "Agreement may cause irreparable harm to the Disclosing Party "
            "for which monetary damages alone would be inadequate. "
            "Accordingly, the Disclosing Party shall be entitled to seek "
            "unlimited injunctive relief, specific performance, and any "
            "other equitable remedies, in addition to any other rights or "
            "remedies available at law or in equity, without the necessity "
            "of proving actual damages and without posting any bond or "
            "other security. The Receiving Party waives any right to "
            "challenge the appropriateness of injunctive relief in any "
            "proceeding."
        ),
    ),
]


# ─────────────────────────────────────────────────────────────────────
# Full contract text (assembled from all clauses)
# ─────────────────────────────────────────────────────────────────────

NDA_CONTRACT_TEXT: str = (
    f"{'='*60}\n"
    f"{NDA_TITLE}\n"
    f"{'='*60}\n\n"
    f"Date: {NDA_METADATA['date']}\n"
    f"Parties: {', '.join(NDA_METADATA['parties'])}\n"
    f"Jurisdiction: {NDA_METADATA['jurisdiction']}\n\n"
    + "".join(
        f"{'─'*60}\n"
        f"Section {i+1}: {clause.title}\n"
        f"{'─'*60}\n"
        f"{clause.text}\n\n"
        for i, clause in enumerate(NDA_CLAUSES)
    )
    + f"{'='*60}\n"
    f"END OF AGREEMENT\n"
    f"{'='*60}\n"
)


# ─────────────────────────────────────────────────────────────────────
# Task-specific clause subsets
# ─────────────────────────────────────────────────────────────────────

# Maps task_id -> list of clause IDs to include.
# - task1 (easy):   All 6 clauses — agent only needs to identify/flag.
# - task2 (medium): 4 clauses with unfair terms — agent must redline.
# - task3 (hard):   2 deal-breaker clauses — full negotiation required.
TASK_CLAUSE_IDS: Dict[str, List[str]] = {
    "task1": ["c1", "c2", "c3", "c4", "c5", "c6"],
    "task2": ["c1", "c2", "c3", "c6"],
    "task3": ["c2", "c3"],
}

# Build a quick lookup by clause ID.
_CLAUSE_BY_ID: Dict[str, Clause] = {c.id: c for c in NDA_CLAUSES}


def load_nda_contract(task_id: str) -> Dict[str, Any]:
    """Load the NDA contract for the given task, returning only the
    relevant clause subset.

    Parameters
    ----------
    task_id : str
        One of ``"task1"``, ``"task2"``, or ``"task3"``.

    Returns
    -------
    dict
        Keys: ``contract_id``, ``contract_title``, ``contract_text``,
        ``clauses`` (list of :class:`Clause`), ``metadata``.

    Raises
    ------
    ValueError
        If *task_id* is not recognised.
    """
    if task_id not in TASK_CLAUSE_IDS:
        raise ValueError(
            f"Unknown task_id '{task_id}'. "
            f"Expected one of: {sorted(TASK_CLAUSE_IDS)}"
        )

    clause_ids = TASK_CLAUSE_IDS[task_id]
    clauses = [_CLAUSE_BY_ID[cid] for cid in clause_ids]

    # Build task-specific contract text from the selected clauses only.
    task_text = (
        f"{'='*60}\n"
        f"{NDA_TITLE}\n"
        f"{'='*60}\n\n"
        f"Date: {NDA_METADATA['date']}\n"
        f"Parties: {', '.join(NDA_METADATA['parties'])}\n"
        f"Jurisdiction: {NDA_METADATA['jurisdiction']}\n\n"
        + "".join(
            f"{'─'*60}\n"
            f"Section {i+1}: {clause.title}\n"
            f"{'─'*60}\n"
            f"{clause.text}\n\n"
            for i, clause in enumerate(clauses)
        )
        + f"{'='*60}\n"
        f"END OF AGREEMENT\n"
        f"{'='*60}\n"
    )

    return {
        "contract_id": NDA_METADATA["contract_id"],
        "contract_title": NDA_TITLE,
        "contract_text": task_text,
        "clauses": clauses,
        "metadata": NDA_METADATA,
    }
