from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import QAPair
from .serializers import MongoQuestionPullSerializer, MongoQuestionSerializer
from .mongo import get_db_handle
from graph.builder import build_graph
from utils.env_loader import load_env
import os 
from bson import ObjectId
from bson.errors import InvalidId
from typing import Dict, Any, Optional
import logging
import uuid
from django.utils import timezone

load_env()

logger = logging.getLogger(__name__)


@api_view(["POST"])
def get_role_stacks_levels(request):  # Endpoint to Generate QA And Interview Session
    
    role = request.data.get('role')
    stacks = request.data.get('stacks')
    level = request.data.get('level')
    allowed_candidates = request.data.get('allowed_candidates') 

    if not role or not stacks or not level or not allowed_candidates:
        return Response({"error": "role, stacks, level, and allowed_candidates are required."}, status=400)
    
    graph= build_graph()
    
    inputs = {
        "role": role,
        "stacks": stacks,
        "level": level  
    }
    result = graph.invoke(inputs)

    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    collection = db['qa_pairs']

    qa_pairs = {}
    
    for qa in result["question_answer_pairs"]:
        
        q_id= f"q{str(uuid.uuid4())[:8]}"

        # question = qa['question']
        # answer = qa['answer']
        # qa_pairs.append({'question': question, 'answer': answer})

        qa_pairs[q_id] = {
            'question': qa['question'],
            'answer': qa['answer']
        }
    
    document = {
        "role": role,
        "stack": stacks, 
        "level": level,
        'qa_pairs': qa_pairs,
        "allowed_candidates": allowed_candidates,
        'created': timezone.now()  # Add created timestamp
    }

    inserted_rec= collection.insert_one(document)    

    ID= str(inserted_rec.inserted_id)
    return Response({"status": "success", "message": "Questions and answers generated and saved.", "Session_ID": f"{ID}"})



@api_view(['POST'])
def validate_candidate(request):

    session_id = request.data.get('session_id')
    email = request.data.get('email')

    if not session_id or not email:
        return Response({"error": "session_id and email are required."}, status=400)
    
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

    if email not in allowed:
        return Response({"error": "Candidate not allowed for this session."}, status=403)
    
    return Response({"status": "Authorized", "message": "Welcome to the interview session."})


@api_view(['GET'])
def get_allqa(request):                ## To Display All Questions and Answers
    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    collection = db['qa_pairs']

    docs= list(collection.find())
    
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    
    serializer = MongoQuestionPullSerializer(docs, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def get_single_question(request, requested_id):   ## To Display Single Question and Answers
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

# @api_view()
# def validate_answer(request):


# @api_view()
# def transcribe_answer(request):
