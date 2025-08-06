##graph/schema.py
from typing import TypedDict, List, Optional, Any, Union

class GraphState(TypedDict):
    position: str
    stacks: List[str]
    level: str
    num_questions: int
    question_answer_pairs: List[dict]
    transcribed_text: Optional[List[str]]  # Changed from str to List[str]
    score: Optional[float]
    video_file: Optional[Union[str, Any]] 
    

# class TranscriptionState(TypedDict):
#     video_path: str
#     transcribed_text: str

# class ValidationState(TypedDict):
#     answer: str
#     transcribed_text: str
#     score: float