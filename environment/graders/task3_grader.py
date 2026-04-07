from typing import List, Dict, Any
from ..models import GradeResult, Action

DEAL_BREAKER_CLAUSES = ["c2", "c3"]

class Task3Grader:
    def grade(self, episode_actions: List[Action], episode_state: Dict[str, Any], negotiation_history: List[Any] = None) -> GradeResult:
        clauses = episode_state["observation"]["clauses"]
        
        db_agreements = sum(1 for c in clauses if c["id"] in DEAL_BREAKER_CLAUSES and c["status"] == "agreed")
        other_agreements = sum(1 for c in clauses if c["id"] not in DEAL_BREAKER_CLAUSES and c["status"] == "agreed")
        other_total = max(1, len(clauses) - len(DEAL_BREAKER_CLAUSES))
        
        agreements_score = (db_agreements / 2) * 0.40 + (other_agreements / other_total) * 0.20
        
        # Simple fairness estimate based on task 2 rubric for agreed text
        from .task2_grader import RUBRIC
        fairness_scores = []
        for c in clauses:
            if c["status"] == "agreed" and c["id"] in RUBRIC:
                pt = c.get("current_proposed_text", "").lower()
                if pt:
                    score = sum(rule["score"] for rule in RUBRIC[c["id"]] if rule["check"](pt))
                    fairness_scores.append(score)
                    
        fairness_score = (sum(fairness_scores) / max(1, len(fairness_scores))) * 0.25 if fairness_scores else 0
        
        turns_used = episode_state["observation"]["turn"]
        optimal = len(clauses) * 4
        efficiency_score = max(0, 1 - max(0, turns_used - optimal) / optimal) * 0.15
        
        final_score = agreements_score + fairness_score + efficiency_score
        
        if db_agreements < 2:
            final_score = min(final_score, 0.30)
            
        final_score = min(1.0, final_score)
        
        return GradeResult(
            task_id="task3",
            score=final_score,
            breakdown={"agreements_score": agreements_score, "fairness_score": fairness_score, "efficiency_score": efficiency_score},
            passed=final_score >= 0.45,
            details=[f"DB Agreements: {db_agreements}/2", f"Turns: {turns_used}"]
        )
