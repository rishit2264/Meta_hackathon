from typing import List, Dict, Any
from ..models import GradeResult, Action

RUBRIC = {
    "c1": [
        {"check": lambda t: ("year" in t or "month" in t) and "perpetuity" not in t, "score": 0.33},
        {"check": lambda t: "specific" in t or "categories" in t or "defined" in t, "score": 0.33},
        {"check": lambda t: len(t.split()) > 15, "score": 0.34},
    ],
    "c2": [
        {"check": lambda t: any(x in t for x in ["12 month","one year","6 month"]), "score": 0.33},
        {"check": lambda t: "global" not in t and ("specific" in t or "schedule" in t), "score": 0.33},
        {"check": lambda t: "future products" not in t, "score": 0.34},
    ],
    "c3": [
        {"check": lambda t: "prior" in t or "pre-existing" in t or "carve-out" in t, "score": 0.34},
        {"check": lambda t: "conceived" in t and "confidential" in t, "score": 0.33},
        {"check": lambda t: "regardless" not in t, "score": 0.33},
    ],
    "c6": [
        {"check": lambda t: "reasonable" in t or "proportional" in t or "cap" in t, "score": 0.50},
        {"check": lambda t: "unlimited" not in t, "score": 0.50},
    ],
}

class Task2Grader:
    def grade(self, episode_actions: List[Action], episode_state: Dict[str, Any]) -> GradeResult:
        propose_actions = [a for a in episode_actions if a.action_type == "propose"]
        
        scores = []
        short_penalty = 0
        
        for c_id in ["c1", "c2", "c3", "c6"]:
            action = next((a for a in propose_actions if a.clause_id == c_id), None)
            if not action or not action.proposed_text:
                scores.append(0.0)
                continue
                
            pt = action.proposed_text.lower()
            c_score = sum(rule["score"] for rule in RUBRIC[c_id] if rule["check"](pt))
            scores.append(c_score)
            
            # rough penalty check
            original_len = len([c for c in episode_state["observation"]["clauses"] if c["id"] == c_id][0]["text"])
            if len(pt) < original_len * 0.5:
                short_penalty += 0.10

        avg_score = sum(scores) / 4 if scores else 0
        bonus = 0.05 if len(scores) == 4 and all(s > 0 for s in scores) else 0.0
        
        final_score = max(0.0, min(1.0, avg_score + bonus - short_penalty))
        
        return GradeResult(
            task_id="task2",
            score=final_score,
            breakdown={"avg_score": avg_score, "bonus": bonus, "short_penalty": short_penalty},
            passed=final_score >= 0.65,
            details=[f"Clause scores: {scores}"]
        )
