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
    created_by: str
    scheduled: str

class CandidateGraphState(TypedDict):
    interview_id: str
    candidate_id: str
    position:str
    candidate_mail: Optional[str]
    candidate_name: Optional[str]
    video_files: List[str]
    transcribed_text: List[str]
    responses: List[str]
    question_answer_pair: Optional[List[dict]]
    scores: Optional[List[float]]

