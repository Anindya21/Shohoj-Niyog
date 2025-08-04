from graph.schema import GraphState
from typing import Optional, List



def create_default_state(**overrides)-> GraphState:
    default_state= {

        "position": "",
        "stacks": [],
        "level": "",
        "question_answer_pairs": [],
        "transcribed_text": [],
        "score": None,
        "video_file": None
}
    default_state.update(overrides)

    return default_state


def create_qa_generation_state(position: str, stacks: List[str], level: str)-> GraphState:
    return create_default_state(
        position=position,
        stacks=stacks,
        level=level
    )

def create_transcription_state(video_file_path: str) -> GraphState:
    """Create state specifically for transcription"""
    return create_default_state(
        video_file=video_file_path
    )

def create_full_workflow_state(position: str, stacks: List[str], level: str, video_file_path: str) -> GraphState:
    """Create state for complete workflow"""
    return create_default_state(
        position=position,
        stacks=stacks,
        level=level,
        video_file=video_file_path
    )