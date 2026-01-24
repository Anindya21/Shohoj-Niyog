import uuid
import os
from bson import ObjectId
from datetime import timedelta
from django.utils import timezone
from logics.db.mongo import get_db_handle
from logics.graph.schema import RecruiterGraphState
from django.utils.dateparse import parse_datetime


def save_qa_pairs_node(state: RecruiterGraphState)-> RecruiterGraphState:
    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    collection = db['qa_pairs']

    qa_pairs = []
        
    for qa in state["question_answer_pairs"]:
        qa_pairs.append({
                'question_id': f"q{str(uuid.uuid4())[:8]}",
                'question': qa['question'],
                'answer': qa['answer']
            })
        
    document = {
            "position": state["position"],
            "stack": state["stacks"], 
            "level": state["level"],
            "company": state["company"],
            "created_by": state["created_by"],
            "qa_pairs": qa_pairs,
            "question_count": len(qa_pairs),
            "allowed_candidates": state["allowed_candidates"],
            "created": timezone.now(),
            "scheduled": parse_datetime(state["scheduled"]),
            "status": "pending" 
        }
        
    inserted_rec= collection.insert_one(document)    

    interview_id= str(inserted_rec.inserted_id)

    return{
        **state,
        "question_answer_pairs":qa_pairs,
        "interview_id": interview_id
    }


