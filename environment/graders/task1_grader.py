from typing import List, Dict, Any
from ..models import GradeResult, Action

GROUND_TRUTH = {
    "c1": {"label": "unfair", "reason": "ip", "deal_breaker": False},
    "c2": {"label": "unfair", "reason": "scope", "deal_breaker": True},
    "c3": {"label": "unfair", "reason": "ip", "deal_breaker": True},
    "c4": {"label": "neutral", "reason": "jurisdiction", "deal_breaker": False},
    "c5": {"label": "fair", "reason": "duration", "deal_breaker": False},
    "c6": {"label": "unfair", "reason": "liability", "deal_breaker": False},
}

class Task1Grader:
    def grade(self, episode_actions: List[Action], episode_state: Dict[str, Any]) -> GradeResult:
        flag_actions = [a for a in episode_actions if a.action_type == "flag"]
        
        correct_labels = sum(1 for a in flag_actions if GROUND_TRUTH[a.clause_id]["label"] == a.label)
        label_score = (correct_labels / 6) * 0.50
        
        correct_reasons = sum(1 for a in flag_actions if a.label == "unfair" and a.reason and GROUND_TRUTH[a.clause_id]["reason"] in a.reason.lower())
        flagged_unfair = sum(1 for a in flag_actions if a.label == "unfair")
        reason_score = (correct_reasons / max(1, flagged_unfair)) * 0.25
        
        db_found = sum(1 for a in flag_actions if a.label == "unfair" and GROUND_TRUTH[a.clause_id]["deal_breaker"])
        db_score = (db_found / 2) * 0.25
        
        false_positives = sum(1 for a in flag_actions if a.label == "unfair" and GROUND_TRUTH[a.clause_id]["label"] != "unfair")
        fp_penalty = false_positives * 0.10
        
        final_score = max(0.0, min(1.0, label_score + reason_score + db_score - fp_penalty))
        
        return GradeResult(
            task_id="task1",
            score=final_score,
            breakdown={
                "label_score": label_score,
                "reason_score": reason_score,
                "db_score": db_score,
                "fp_penalty": fp_penalty
            },
            passed=final_score >= 0.85,
            details=[f"Correct labels: {correct_labels}/6", f"Deal breakers found: {db_found}/2"]
        )
