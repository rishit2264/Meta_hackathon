"""
ContractEnv — Legal Contract Negotiation RL Environment
========================================================

An OpenEnv-compliant reinforcement learning environment where an AI agent
negotiates business contracts clause by clause.

Quick start
-----------
::

    from environment import (
        Clause, ClauseCategory, ClauseLabel,
        Action, ActionType, Observation, Reward,
    )

    # Build an action
    action = Action(
        clause_id="clause-001",
        action_type=ActionType.FLAG,
        label=ClauseLabel.UNFAIR,
        reason="Liability cap is unreasonably low.",
    )

    # Once the environment module is ready:
    # from environment import ContractEnv
    # env = ContractEnv()
    # obs = env.reset(task_id="task1")
    # obs, reward = env.step(action)
"""

__version__ = "1.0.0"
__author__ = "ContractEnv Team — Meta / Scaler OpenEnv Hackathon"

# ── Public model imports ─────────────────────────────────────────────
from .models import (
    Action,
    ActionType,
    Clause,
    ClauseCategory,
    ClauseLabel,
    CounterpartyState,
    NegotiationTurn,
    Observation,
    Reward,
    RewardBreakdown,
    TaskConfig,
)

# ── Environment import (graceful stub until Phase 2) ─────────────────
try:
    from .env import ContractEnv  # type: ignore[import-not-found]
except ImportError:
    # ContractEnv will be implemented in Phase 2.  Provide a sentinel
    # so that downstream code can check `if ContractEnv is not None`.
    ContractEnv = None  # type: ignore[assignment, misc]

# ── Public API ───────────────────────────────────────────────────────
__all__ = [
    # Environment
    "ContractEnv",
    # Enums
    "ClauseCategory",
    "ClauseLabel",
    "ActionType",
    "CounterpartyState",
    # Data models
    "Clause",
    "NegotiationTurn",
    "Observation",
    "Action",
    "RewardBreakdown",
    "Reward",
    "TaskConfig",
]
