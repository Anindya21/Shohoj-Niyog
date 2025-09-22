from logics.graph.schema import CandidateGraphState
from logics.db.mongo import get_db_handle
import os
from bson.objectid import ObjectId

# Load the question-answer pairs along with question ID for a candidate's interview session

def load_qa_node(state: CandidateGraphState) -> CandidateGraphState:
    
    interview_id = state.get("interview_id")
    
    if not interview_id:
        print("No Session ID provided.")
        return {
            **state,
            "question_answer_pairs": []
        }

    try:
        uri = os.getenv("mongo_uri")
        db, _ = get_db_handle("interview_db")
        collection = db['qa_pairs']

        session= collection.find_one({"_id": ObjectId(interview_id)})

        if not session:
            print(f"No interview Session found for {interview_id}")
            return {
                **state,
                "question_answer_pairs": []
            }
        
        question_data = []
    
        qa_pairs = session.get("qa_pairs", [])
        position = session.get("position", "")

        for qa in qa_pairs:
            question_data.append({
                "question_id": qa.get("question_id"),
                "question": qa.get("question"),
                "expected_answer": qa.get("answer")
            })

        print(f"Loaded {interview_id} sessions relevant data")

        return{
            **state,
            "question_answer_pairs": question_data,
            "position": position,

        }

    except:
        print("Failed to load session data from MongoDB.")
        return{
            **state,
            "question_answer_pairs":[]
        }