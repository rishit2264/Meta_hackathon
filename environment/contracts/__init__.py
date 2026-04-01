"""
ContractEnv Phase 2 — Contracts Package
========================================

Exports the NDA contract template and provides a unified
``load_contract`` entry point used by :class:`environment.env.ContractEnv`.
"""

from __future__ import annotations

from typing import Any, Dict

from .nda_template import (
    NDA_CLAUSES,
    NDA_CONTRACT_TEXT,
    NDA_METADATA,
    NDA_TITLE,
    TASK_CLAUSE_IDS,
    load_nda_contract,
)

__all__ = [
    "NDA_CLAUSES",
    "NDA_CONTRACT_TEXT",
    "NDA_METADATA",
    "NDA_TITLE",
    "TASK_CLAUSE_IDS",
    "load_nda_contract",
    "load_contract",
]


def load_contract(task_id: str) -> Dict[str, Any]:
    """Unified contract loader — the main entry point for ``env.py``.

    Currently delegates to :func:`load_nda_contract`.  Future phases
    can add additional templates (SaaS agreement, partnership deed,
    etc.) and route based on *task_id*.

    Parameters
    ----------
    task_id : str
        One of ``"task1"``, ``"task2"``, ``"task3"``.

    Returns
    -------
    dict
        Contract data with keys ``contract_id``, ``contract_title``,
        ``contract_text``, ``clauses``, ``metadata``.
    """
    return load_nda_contract(task_id)
