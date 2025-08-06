##graph/schema.py
from typing import TypedDict, List, Optional, Any, Union

class RecruiterGraphState(TypedDict):
    position: str
    stacks: List[str]
    level: str
    num_questions: int
    question_answer_pairs: List[dict]
    interview_id: Optional[str]
    allowed_candidates: List[str]

class CandidateGraphState(TypedDict):
    interview_id: str
    candidate_id: str
    transcribed_text: List[str]
    question_answer_pair: List[dict]
    score: Optional[List[float]]

