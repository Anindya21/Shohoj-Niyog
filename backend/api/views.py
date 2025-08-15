from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import QAPair
from .serializers import MongoQuestionPullSerializer, MongoQuestionSerializer, CandidateSessionsSerializer
from db.mongo import get_db_handle
from graph.builder import build_recruiter_graph, build_candidate_graph
from utils.env_loader import load_env
from bson import ObjectId
from bson.errors import InvalidId
from typing import Dict, Any, Optional
from django.utils import timezone
# from datetime import datetime,timezone  
import os, uuid, logging, mimetypes, tempfile
from rest_framework import status

load_env()

logger = logging.getLogger(__name__)

##backend/api/views.py
recruiter_graph= build_recruiter_graph()
candidate_graph= build_candidate_graph()

#================================== Interviewer =======================================

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_interview_session(request):  # Endpoint to Generate QA And Interview Session
    
    user= request.user
    
    if user.role == "candidate":
        return Response({"message": "Unauthorized Action"}, status=403)
    
    position = request.data.get('position')
    stacks = request.data.get('stacks')
    level = request.data.get('level')
    allowed_candidates = request.data.get('allowed_candidates')
    num_questions= request.data.get('num_questions')
    scheduled= request.data.get('scheduled', timezone.now().isoformat())

    if not position or not stacks or not level or not allowed_candidates:
        return Response({"error": "position, stacks, level, and allowed_candidates are required."}, status=400)
    
    inputs= {
            "position": position,
            "stacks": stacks,
            "level": level,
            "num_questions":num_questions,
            "allowed_candidates":allowed_candidates,
            "created_by": str(user.id),
            "scheduled":  scheduled
            }
    
    result = recruiter_graph.invoke(inputs)

    return Response({"status": "success", "message": "Questions and answers generated and saved.", 
                     "Session_ID": result["interview_id"], 
                     "Created_By": str(user.id)}, 
                     status=status.HTTP_201_CREATED)
# ===================================================================================================


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_allqa(request, requested_id):  ## To Display All Questions and Answers
    
    user= request.user               
    
    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    collection = db['qa_pairs']

    if user.role == "candidate":

        docs= list(collection.find(
            {"allowed_candidates": 
             {"$in": [str(user.id), user.email]}
             }))

        for doc in docs:
            doc['_id'] = str(doc['_id'])
        
        serializer= CandidateSessionsSerializer(docs, many=True)
        
        return Response(serializer.data)
    
    user_id= str(user.id)


    

    docs= list(collection.find({'created_by': user_id}))
    
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    
    serializer = MongoQuestionPullSerializer(docs, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def get_single_question(request, requested_id):   ## To Display Single Question and Answers
    
    # user= request.user               
    
    # if user.role == "candidate":
    #     return Response({"message": "Unauthorized Action"}, status=403)
    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    collection = db['qa_pairs']

    try:
        docs= collection.find_one({'_id': ObjectId(requested_id)})
    except Exception as e:
        return Response({"error": "Invalid ID format."}, status=400)
    
    if not docs:
        return Response({"error": "Document not found."}, status=404)
    
    qa_pairs = docs.get("qa_pairs", [])

    serializer = MongoQuestionSerializer(qa_pairs, many=True)
    return Response(serializer.data)

# =============================== Candidate =========================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_candidate(request):

    user = request.user

    session_id = request.data.get('session_id')
    user_id = str(user.id)

    if not session_id:
        return Response({"error": "session_id is required."}, status=400)
    
    try:
        uri = os.getenv("mongo_uri")
        db, _ = get_db_handle("interview_db")
        collection = db['qa_pairs']

        session_doc = collection.find_one({'_id': ObjectId(session_id)})
    except:
        return Response({"error": "Invalid session_id format."}, status=400)

    if not session_doc:
        return Response({"error": "Session not found."}, status=404) 
    
    allowed = session_doc.get('allowed_candidates', [])

    if user_id not in allowed:
        return Response({"error": "Candidate not allowed for this session."}, status=403)
    
    return Response({"status": "Authorized", "message": "Welcome to the interview session."})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_response(response):
    user = response.user

    user_id = str(user.id)
    user_mail = user.email
    session_id = response.data.get("session_id")
    user_name = user.get_full_name() or user.username

    
    if not session_id:
        return Response({"error": "session_id is required."}, status=400)
    
    if user.role != "candidate":
        return Response({"message": "You Must be a candidate to join an interview"}, status=status.HTTP_403_FORBIDDEN)
    
    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    qa_col = db['qa_pairs']


    allowed_candidates= qa_col.find_one({'_id': ObjectId(session_id)}).get('allowed_candidates', [])

    if user_id not in allowed_candidates:
        return Response({"error": "You are not allowed to join this session."}, status=403)
    

    video_files = response.FILES.getlist("video")

    if not video_files:
        return Response({"error": "video_files is required."}, status=400)
    

    temp_video_paths = []

    try:

        for i, video_file in enumerate(video_files):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)
                temp_video_paths.append(temp_file.name)

        
        inputs= {
            "interview_id": session_id,
            "candidate_id": user_id,
            "candidate_name": user_name,
            "candidate_mail": user_mail,
            "video_files": temp_video_paths,
            "transcribed_text": [],
            "question_answer_pair": [],
            "responses": [],
            "total_score": None,
            "allowed_candidates": []
            }
        
        result = candidate_graph.invoke(inputs)

        if result.get("save_status") == "success":
            return Response({
                "status": "success",
                "message": "Responses saved successfully. Thank you for joining the interview session.",
                "responsed_id": result.get("responsed_id")

            })
        
        else:
            return Response({"error": "Failed to save responses"}, status=500)
        

    except Exception as e:
        return Response({"error": str(e)}, status=500)
    

    finally:
        for temp_path in temp_video_paths:
            if os.path.exists(temp_path):
                os.unlink(temp_path)


    
    # try:
    #     session_doc = qa_col.find_one({'_id': ObjectId(session_id)})

    #     return Response({"status": "success", "message": "Session found."})

    # except:
    #     return Response({"error": "Invalid session_id format."}, status=400)

