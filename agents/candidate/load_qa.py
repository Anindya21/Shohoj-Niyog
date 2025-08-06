from graph.schema import CandidateGraphState
from db.mongo import get_db_handle
import os

def load_qa_node(state: CandidateGraphState) -> CandidateGraphState:
    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    collection = db['qa_pairs']

    result=collection.find_one({"interview_id": state["interview_id"]})

    return{
        **state,
        "question_answer_pair":result["qa_pairs"]
    }