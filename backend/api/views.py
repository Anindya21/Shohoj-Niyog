from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from .models import QAPair
from .serializers import (MongoQuestionPullSerializer, MongoQuestionSerializer, 
                          CandidateSessionsSerializer, CandidateResultSerializer, 
                          CandidateOwnResultSerializer, CandidateAllSessionsSerializer)

from logics.db.mongo import get_db_handle
from logics.graph.builder import build_recruiter_graph, build_candidate_graph
from logics.utils.env_loader import load_env
from bson import ObjectId
from bson.errors import InvalidId
from typing import Dict, Any, Optional
from django.utils import timezone
import os, uuid, logging, mimetypes, tempfile
from rest_framework import status
from functools import lru_cache


from logics.utils.tasks import run_candidate_graph

load_env()

logger = logging.getLogger(__name__)

@lru_cache(maxsize=1)
def get_recruiter_graph():
    return build_recruiter_graph()


def to_object_id(id_str):
    if not ObjectId.is_valid(id_str):
        raise InvalidId("Invalid ObjectId")
    return ObjectId(id_str)

def session_id_query(session_id):
    try:
        return {"$in": [session_id, to_object_id(session_id)]}
    except InvalidId:
        return session_id
    
## Interview Session Generation API View

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def generate_interview_session(request):  # Endpoint to Generate QA And Interview Session
    
    user= request.user
    
    print(user.company)
    if user.role == "candidate":
        return Response({"message": "Unauthorized Action"}, status=403)
    
    position = request.data.get('position')
    stacks = request.data.get('stacks')
    level = request.data.get('level')
    allowed_candidates = request.data.get('allowed_candidates')
    num_questions= request.data.get('num_questions')
    scheduled= request.data.get('scheduled', timezone.now().isoformat())
    company=user.company
    
    if not position or not stacks or not level or not allowed_candidates:
        return Response({"error": "position, stacks, level, and allowed_candidates are required."}, status=400)
    
    inputs= {
            "position": position,
            "stacks": stacks,
            "level": level,
            "num_questions":num_questions,
            "allowed_candidates":allowed_candidates,
            "company": str(company),
            "created_by": str(user.id),
            "scheduled":  scheduled
            }
    
    result = get_recruiter_graph().invoke(inputs)

    return Response({"status": "success", "message": "Questions and answers generated and saved.", 
                     "Session_ID": result["interview_id"], 
                     "Company": str(company)}, 
                     status=status.HTTP_201_CREATED)

## Api View For Recruiter: Show ALL the Sessions and Details, Candidate: Views the Sessions Assigned to them

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_allqa(request):  ## To Display All Questions and Answers
    
    user= request.user               
    db, _ = get_db_handle("interview_db")
    collection = db["qa_pairs"]


    try:
        limit= min(int(request.GET.get('limit',50)),200)
        skip = max(int(request.GET.get('skip',0)),0)

    except ValueError:
        limit,skip= 50,0

    if user.role == "candidate":

        docs= list(collection.find(
            {"allowed_candidates": 
             {"$in": [str(user.id), user.email]}},
             projection={'qa_pairs':0}
             ).skip(skip).limit(limit)
             )

        for doc in docs:
            doc['_id'] = str(doc['_id'])
        
        serializer= CandidateAllSessionsSerializer(docs, many=True)
        
        return Response(serializer.data, status= status.HTTP_200_OK)
    
    user_id= str(user.id)

    docs= list(collection.find(
        {'created_by': user_id},
        projection={'qa_pairs': 0}).skip(skip).limit(limit))
    
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    
    serializer = MongoQuestionPullSerializer(docs, many=True)
    
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_single_question(request, session_id):   ## To Display Single Question and Answers
    
    user= request.user 
    db, _ = get_db_handle("interview_db")
    collection = db["qa_pairs"]


    try:
        oid = to_object_id(session_id)
    except InvalidId:
        return Response({"error": "Invalid ID format."}, status=status.HTTP_400_BAD_REQUEST)

    
    if user.role !="candidate":
        docs= collection.find_one({'_id': oid})
        
        if not docs:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        
        docs['_id'] = str(docs['_id'])
        serializer= MongoQuestionPullSerializer(docs, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    else:
        docs= collection.find_one({'_id':oid}, projection= {'qa_pairs':1, '_id':0})
        if not docs:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
         
        qa_pairs = docs.get("qa_pairs", [])

        serializer = MongoQuestionSerializer(qa_pairs, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validate_candidate(request):

    user = request.user
    session_id = request.data.get('session_id')
    user_id = str(user.id)

    if not session_id:
        return Response({"error": "session_id is required."}, status=400)
    
    try:
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

## Candidate Response API View

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def user_response(request):
    user = request.user

    if user.role != "candidate":
        return Response({"message": "You Must be a candidate to join an interview"}, status=status.HTTP_403_FORBIDDEN)
    
    user_id = str(user.id)
    user_mail = user.email
    session_id = request.data.get("session_id")
    user_name = user.get_full_name() or user.username

    if not session_id:
        return Response({"error": "session_id is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        session_oid = to_object_id(session_id)
    except InvalidId:
        return Response({"error": "Invalid session_id format."}, status=status.HTTP_400_BAD_REQUEST)

    
    db, _ = get_db_handle("interview_db")
    qa_col = db["qa_pairs"]
    user_col = db["user_db"]


    docs= qa_col.find_one({'_id': session_oid}, projection={'allowed_candidates': 1})
    if not docs:
        return Response({"error": "Session not found."}, status=status.HTTP_404_NOT_FOUND)

    allowed_candidates= set(docs.get('allowed_candidates',[]))

    if user_id not in allowed_candidates and user_mail not in allowed_candidates:
        return Response({"error": "You are not allowed to join this session."}, status=status.HTTP_403_FORBIDDEN)
    
    prev_response = user_col.find_one(
        {'session_id': session_oid, 'candidate_id': user_id}
    )

    if prev_response:
        status_ = prev_response.get("status")

        if status_ == "processing":
            return Response(
            {
                "status": "processing",
                "message": "Your responses are already being processed."
            },
            status=status.HTTP_202_ACCEPTED
            )

        if status_ == "completed":
            return Response(
            {
                "message": "You have already submitted your responses for this session."
            },
            status=status.HTTP_403_FORBIDDEN
            )


    video_files = request.FILES.getlist("video")

    if not video_files:
        return Response({"error": "video_files is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    temp_video_paths = []

    try:
        for i, video_file in enumerate(video_files):
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                for chunk in video_file.chunks():
                    temp_file.write(chunk)
                temp_video_paths.append(temp_file.name)
      
        inputs= {
            "interview_id": str(session_oid),
            "candidate_id": user_id,
            "candidate_name": user_name,
            "candidate_mail": user_mail,
            "video_files": temp_video_paths,
            "transcribed_text": [],
            "question_answer_pairs": [],
            "responses": [],
            "total_score": None,
            "allowed_candidates": []
            }
        
        user_col.insert_one({
            "session_id": session_oid,
            "candidate_id": user_id,
            "candidate_name": user_name,
            "candidate_mail": user_mail,
            "status": "processing",
            "created_at": timezone.now()
            })
        run_candidate_graph.delay(inputs)


        return Response({
                    "status": "accepted",
                    "message": "Responses are being processed"
        }, status=status.HTTP_202_ACCEPTED)
        
    except Exception as e:
        logger.exception("user_response failed")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# Session Results View for both Candidate and Recruiter

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_session_results(request, session_id=None):

    user=request.user

    db, _ = get_db_handle("interview_db")
    collection = db["user_db"]


    if user.role=="interviewer": 

        if not session_id:
            return Response({"error": "session_id is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            session_oid = ObjectId(session_id)
            query = {"session_id": session_oid}
        except Exception:
            query = {"session_id": session_id}

        docs = list(collection.find(query))



        for doc in docs:
            doc['_id'] = str(doc['_id'])
            doc['session_id'] = str(doc['session_id'])
            doc['candidate_id'] = str(doc['candidate_id'])
            for response in doc.get('responses', []):
                response['question_id'] = str(response['question_id'])


        serializer= CandidateResultSerializer(docs, many=True)
        
        return Response(serializer.data, status= status.HTTP_200_OK)


    if user.role!='interviewer':

        docs = list(
            collection.find(
                {"candidate_mail": user.email}).sort("created_at", -1)
                )
        print(docs)
            
        for doc in docs:
            doc['_id'] = str(doc['_id'])
            doc['session_id'] = str(doc['session_id'])
            doc['candidate_id'] = str(doc['candidate_id'])
                
            for response in doc.get('responses', []):
                response['question_id'] = str(response['question_id'])

        
        serializer = CandidateOwnResultSerializer(docs, many=True)

        if not serializer.data:
            return Response({"message": "Candidate has not given any response yet."}, status=status.HTTP_204_NO_CONTENT)

        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
## Hiring Decision API View Recruiter: Can Show interest in a candidate,
@api_view(['PATCH'])    ## Need to update this, PUT or PATCH
@permission_classes([IsAuthenticated])
def hiring_decision(request):
    user = request.user
    session_id = request.data.get('session_id')
    candidate_id = request.data.get('candidate_id')
    decision= request.data.get('decision')

    if not session_id or not decision:
            return Response({"error": "session_id and decision are required."}, status=status.HTTP_400_BAD_REQUEST)
    

    if decision not in ["interested","not_interested", "accept","reject"]:
            return Response({"error": "decision must be 'interested','not_interested', 'accept' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)
    
    db, _ = get_db_handle("interview_db")
    collection = db['user_db']

    
    if user.role != "candidate":
        # Consider pending also
        if not session_id or not candidate_id or not decision:
            return Response({"error": "session_id, candidate_id and decision are required."}, status=status.HTTP_400_BAD_REQUEST)
     
        if decision not in ["interested", "not_interested"]:
            return Response({"error": "Your only option as a recruiter is interested or not interested."}, status=status.HTTP_400_BAD_REQUEST)
        
        
        responses = collection.find_one( {"session_id": session_id_query(session_id), "candidate_id": candidate_id})

        if not responses:
            return Response("No responses found for this session and candidate.", status=status.HTTP_404_NOT_FOUND)


        result =  collection.update_one(
            {"session_id":session_id_query(session_id), "candidate_id": candidate_id},
            {"$set": {"decision": decision}}
        )
        
        return Response(
            {"message": f"Successfully updated the hiring decision for the candidate {candidate_id} in session {session_id}."},
            status=status.HTTP_200_OK
        )

    if user.role == "candidate":

        if decision not in ["accept", "reject"]:
            return Response({"error": "Your only option as a candidate is accept or reject."}, status=status.HTTP_403_FORBIDDEN)
            
        responses = collection.find_one( {"session_id": session_id_query(session_id), "candidate_id": str(user.id)})

        print(responses)

        if not responses:
            return Response("No responses found for this session and candidate.", status=404)

        rec_decision = responses.get("decision")

        if rec_decision=="pending":
            return Response({"message": "Your interview is still under review by the recruiter."}, status=status.HTTP_200_OK)
            
        elif rec_decision == "interested" and decision == "accept":
                
            result = collection.update_one(
                {"session_id":session_id_query(session_id), "candidate_id": str(user.id)},
                    {"$set": {"decision": decision}}
                    )
                
            return Response({"message": f"Congratulations! You have made your decision to {decision} the offer."}, status=status.HTTP_200_OK)

        elif rec_decision == "interested" and decision == "reject":
            result = collection.update_one(
                    {"session_id":session_id_query(session_id), "candidate_id": str(user.id)},
                    {"$set": {"decision": decision}}
                    )

            return Response({"message": f"You have decided to {decision} the offer. Thank you for your time."}, status=status.HTTP_200_OK)
            
        elif rec_decision == "not_interested":
            return Response({"message": "Sorry, you couldn't match our vibe. Wish you all the best!"}, status=status.HTTP_200_OK)
