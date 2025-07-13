from typing import TypedDict, List

class GraphState(TypedDict):
    role: str
    stacks: List[str]
    level: str
    # questions: List[str]
    # answers:List[str]
    question_answer_pairs: List[dict]
