from typing import TypedDict, List

class GraphState(TypedDict):
    role: str
    stacks: List[str]
    level: str
    question_answer_pairs: List[dict]
