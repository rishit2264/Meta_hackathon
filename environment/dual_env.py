from typing import List, Tuple, Dict
from copy import deepcopy
from .models import NegotiationSession, NegotiationRole, Observation, Action, NegotiationTurn

class DualAgentEnv:
    def __init__(self, session: NegotiationSession):
        self.session = session
        self.clauses = {c.id: c for c in session.clauses}
        
    def get_observation(self, role: NegotiationRole) -> Observation:
        obs = Observation(
            contract_id=self.session.contract_id,
            contract_title=self.session.contract_title,
            contract_text="",
            clauses=list(self.clauses.values()),
            negotiation_history=self.get_private_history(role),
            current_clause_id=None,
            turn=self.session.turn,
            max_turns=self.session.max_turns,
            task_id="dual",
            agreements_reached=sum(1 for c in self.clauses.values() if c.status == "agreed"),
            total_clauses=len(self.clauses),
            session_id=self.session.session_id,
            role=role
        )
        return obs
        
    def step_seller(self, action: Action) -> Tuple[Observation, float, bool]:
        return self._step(NegotiationRole.seller, action)
        
    def step_client(self, action: Action) -> Tuple[Observation, float, bool]:
        return self._step(NegotiationRole.client, action)
        
    def _step(self, role: NegotiationRole, action: Action) -> Tuple[Observation, float, bool]:
        self.session.turn += 1
        clause = self.clauses.get(action.clause_id)
        
        turn = NegotiationTurn(
            turn_number=self.session.turn,
            speaker=f"{role.value}_agent", # seller_agent or client_agent
            action_type=action.action_type,
            clause_id=action.clause_id,
            content=f"{role.value.capitalize()} proposed redline." if action.action_type == "propose" else f"{role.value.capitalize()} {action.action_type}s.",
            proposed_text=action.proposed_text,
            internal_reasoning=action.internal_reasoning,
            is_visible_to_both=True
        )
        self.session.negotiation_history.append(turn)
        
        if action.action_type == "propose" and action.proposed_text:
            clause.current_proposed_text = action.proposed_text
            clause.status = "in_negotiation"
        elif action.action_type == "accept":
            clause.status = "agreed"
            self.session.final_agreed_clauses[action.clause_id] = clause.current_proposed_text
            self.session.negotiation_history.append(NegotiationTurn(
                turn_number=self.session.turn,
                speaker="system",
                action_type="accept",
                clause_id=action.clause_id,
                content=f"Agreement reached on Clause {action.clause_id} ✓",
            ))
            
        done = self.is_complete()
        if done:
            self.session.status = "completed"
            
        return self.get_observation(role), 0.0, done
        
    def get_full_history(self) -> List[NegotiationTurn]:
        return self.session.negotiation_history
        
    def get_private_history(self, role: NegotiationRole) -> List[NegotiationTurn]:
        # Filter internal reasoning of the opponent
        history = deepcopy(self.session.negotiation_history)
        for t in history:
            if t.speaker != f"{role.value}_agent" and t.speaker != "system":
                t.internal_reasoning = None
        return history
        
    def is_complete(self) -> bool:
        agreed = sum(1 for c in self.clauses.values() if c.status == "agreed")
        if agreed == len(self.clauses) or self.session.turn >= self.session.max_turns:
            return True
        return False
        
    def get_final_contract(self) -> str:
        text_parts = []
        for c in self.clauses.values():
            text_parts.append(f"{c.title}:")
            if c.status == "agreed" and c.id in self.session.final_agreed_clauses:
                text_parts.append(self.session.final_agreed_clauses[c.id])
            else:
                text_parts.append(c.text)
        return "\n\n".join(text_parts)
