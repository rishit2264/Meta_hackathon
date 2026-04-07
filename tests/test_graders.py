from environment.graders.task1_grader import Task1Grader
from environment.graders.task2_grader import Task2Grader
from environment.graders.task3_grader import Task3Grader
from environment.models import Action

def test_task1_grader():
    grader = Task1Grader()
    actions = [Action(clause_id="c1", action_type="flag", label="unfair", reason="ip")]
    episode_state = {}
    result = grader.grade(actions, episode_state)
    assert result.task_id == "task1"

def test_task2_grader():
    grader = Task2Grader()
    actions = [Action(clause_id="c1", action_type="propose", proposed_text="1 year")]
    episode_state = {"observation": {"clauses": [{"id": "c1", "text": "foo"}]}}
    result = grader.grade(actions, episode_state)
    assert result.task_id == "task2"

def test_task3_grader():
    grader = Task3Grader()
    actions = []
    episode_state = {"observation": {"turn": 5, "clauses": [{"id": "c2", "status": "agreed"}]}}
    history = []
    result = grader.grade(actions, episode_state, history)
    assert result.task_id == "task3"
