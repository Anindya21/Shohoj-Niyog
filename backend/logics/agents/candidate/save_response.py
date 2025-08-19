from logics.graph.schema import CandidateGraphState
from logics.db.mongo import get_db_handle
from datetime import datetime,timezone
import os

def save_response_node(state: CandidateGraphState) -> CandidateGraphState:
    
    try:
    
        uri = os.getenv("mongo_uri")
        db, _ = get_db_handle("interview_db")
        can_col = db['user_db']
        rec_col = db["qa_pairs"]

        qa_pairs = state.get("question_answer_pair", [])
        transcribed_text = state.get("transcribed_text", [])
        scores= state.get("scores", [])
        interview_id = state.get("interview_id")
        candidate_id = state.get("candidate_id")
        candidate_mail = state.get("candidate_mail", None)
        candidate_name = state.get("candidate_name", None)
        position = state.get("position", None)

        if not interview_id or not candidate_id:
            print("No interview ID or candidate ID provided.")
            return {
                **state,
                "transcribed_text": [],
                "scores": []
            }
        

        responses= []

        for ques_data, given, score in zip(qa_pairs,transcribed_text, scores):
            responses.append(
                {   "question_id": ques_data.get("question_id"),
                    "given_answer": given,
                    "score": score
                }
            )

        average_score = sum(scores)/ len(scores)

        
        result= can_col.insert_one({
            "session_id": interview_id,
            "position":position,
            "candidate_id": candidate_id,
            "candidate_name": candidate_name,
            "candidate_mail": candidate_mail,
            "responses": responses,
            "total_score": average_score,
            "decision": "pending",
            "created": datetime.now(timezone.utc)
        })

        print(f"Saved candidate response with ID: {result.inserted_id}")
        
        return {
            **state,
            "transcribed_text": transcribed_text,
            "responses": responses,
            "total_score": average_score,
            "save_status": "success",
            "responsed_id": str(result.inserted_id)
        }
    
    except:
        print("Failed to save candidate response.")
        return {
            **state,
            "save_status": "failed"
        }