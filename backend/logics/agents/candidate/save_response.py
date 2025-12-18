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

        qa_pairs = state.get("question_answer_pairs", [])
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
                    "ideal_answer": ques_data.get("expected_answer"),
                    "given_answer": given,
                    "score": score
                }
            )

        average_score = sum(scores)/ len(scores)

        
        can_col.update_one(
        {"session_id": interview_id, "candidate_id": candidate_id},
        {"$set": {
        "position": position,
        "responses": responses,
        "total_score": average_score,
        "decision": "pending",
        "status": "completed",
        "completed_at": datetime.now(timezone.utc)
        }}
)

        
        
        return {
        **state,
        "responses": responses,
        "total_score": average_score,
        "save_status": "success"
        }
    

    except Exception as e:
        can_col.update_one(
        {"session_id": interview_id, "candidate_id": candidate_id},
        {"$set": {
            "status": "failed",
            "error": str(e),
            "failed_at": datetime.now(timezone.utc)
        }}
    )

        return {
        **state,
        "save_status": "failed"
        }
    
    finally:
        for path in state.get("video_files", []):
            try:
                if os.path.exists(path):
                    os.unlink(path)
            except Exception:
                pass