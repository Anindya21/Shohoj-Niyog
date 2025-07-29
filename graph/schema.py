from typing import TypedDict, List, Optional

class GraphState(TypedDict):
    role: str
    stacks: List[str]
    level: str
    question_answer_pairs: List[dict]
    transcribed_text: Optional[str]
    score: Optional[float]
    

# class TranscriptionState(TypedDict):
#     video_path: str
#     transcribed_text: str

# class ValidationState(TypedDict):
#     answer: str
#     transcribed_text: str
#     score: float