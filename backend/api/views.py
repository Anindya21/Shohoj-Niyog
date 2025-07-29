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

load_env()

logger = logging.getLogger(__name__)

# class InterviewDBService:
#     def __init__ (self):
#         self._db = None
#         self._metadata_collection= None
#         self._qa_pairs_collection = None

#     @property
#     def db(self):
#         if self._db is None:
#             uri = os.getenv("mongo_uri")

#             if not uri:
#                 raise ValueError("MongoDB URI is not set in environment variables.")
#             self._db, _ = get_db_handle("interview_db")
        
#         return self._db
    
#     @property
#     def metadata_collection(self):
#         if self._metadata_collection is None:
#             self._metadata_collection = self.db['interview_metadata']
#         return self._metadata_collection
    
#     @property
#     def qa_pairs_collection(self):
#         if self._qa_pairs_collection is None:
#             self._qa_pairs_collection = self.db['qa_pairs']
#         return self._qa_pairs_collection


#     def save_interview_session(self, role: str, stacks:str, level:str)


@api_view(["POST"])
def get_role_stacks_levels(request):
    
    role = request.data.get('role')
    stacks = request.data.get('stacks')
    level = request.data.get('level')

    if not role or not stacks or not level:
        return Response({"error": "role, stacks, and level are required."}, status=400)
    
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

    qa_pairs = []
    
    for qa in result["question_answer_pairs"]:
        question = qa['question']
        answer = qa['answer']
        qa_pairs.append({'question': question, 'answer': answer})

    inserted_rec= collection.insert_one({"role": role,"stack":stacks, "level":level ,'qa_pairs': qa_pairs})    

    ID= str(inserted_rec.inserted_id)
    return Response({"status": "success", "message": "Questions and answers generated and saved.", "Session_ID": f"{ID}"})

@api_view(['GET'])
def get_allqa(request):
    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    collection = db['qa_pairs']

    docs= list(collection.find())
    
    for doc in docs:
        doc['_id'] = str(doc['_id'])
    
    serializer = MongoQuestionPullSerializer(docs, many=True)
    
    return Response(serializer.data)

@api_view(['GET'])
def get_single_question(request, requested_id):
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

