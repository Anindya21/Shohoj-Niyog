from graph.schema import CandidateGraphState
from db.mongo import get_db_handle
import os

def save_response_node(state: CandidateGraphState) -> CandidateGraphState:
    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    col = db['user_db']

    col.insert_one({
        "interview_id": state["interview_id"],
        "candidate_id": state["candidate_id"],
        "transcribed_text": state["transcribed_text"],
        "score": state["score"]
    })

    return state