from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import QAPair
from .serializers import MongoQuestionPullSerializer, MongoQuestionSerializer
from .mongo import get_db_handle
from graph.builder import build_graph
from utils.state_factory import create_qa_generation_state, create_transcription_state
from utils.env_loader import load_env
from bson import ObjectId
from bson.errors import InvalidId
from typing import Dict, Any, Optional
from django.utils import timezone
import os, uuid, logging, mimetypes, tempfile

load_env()

logger = logging.getLogger(__name__)

##backend/api/views.py
graph= build_graph()

@api_view(["POST"])
def get_role_stacks_levels(request):  # Endpoint to Generate QA And Interview Session
    
    
    position = request.data.get('position')
    stacks = request.data.get('stacks')
    level = request.data.get('level')
    allowed_candidates = request.data.get('allowed_candidates') 

    if request.user.role == "candidate":
        return Response({"message": "Unauthorized Action"})
    else:
        if not position or not stacks or not level or not allowed_candidates:
            return Response({"error": "position, stacks, level, and allowed_candidates are required."}, status=400)
    
    
        inputs = {
            "position": position,
            "stacks": stacks,
            "level": level  
        }
    
        result = graph.invoke(inputs)

        uri = os.getenv("mongo_uri")
        db, _ = get_db_handle("interview_db")
        collection = db['qa_pairs']

        qa_pairs = []
        
        for qa in result["question_answer_pairs"]:
            
            q_id= f"q{str(uuid.uuid4())[:8]}"

            # question = qa['question']
            # answer = qa['answer']
            # qa_pairs.append({'question': question, 'answer': answer})

            qa_pairs.append({
                'question_id': q_id,
                'question': qa['question'],
                'answer': qa['answer']
            })
        
        document = {
            "position": position,
            "stack": stacks, 
            "level": level,
            "qa_pairs": qa_pairs,
            "question_count": len(qa_pairs),
            "allowed_candidates": allowed_candidates,
            "created": timezone.now()  # Add created timestamp
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

@api_view(['POST'])
def user_response(response):         ### Transcribes the response video and stores it in the user's collection database

    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    user_col = db['user_db']
    ques_col = db['qa_pairs']

    video_file = response.data.get("video")
    # ques_ids = response.data.get("question_id")

    if not video_file:
        return Response({"error": "video_file and email are required."}, status=400)

    mime_type, _ = mimetypes.guess_type(response.FILES['video'].name)
    
    if mime_type == 'video/mp4':
        print("Video file is valid. Proceeding with upload...") 
    else:
        return Response({"message": "Invalid video format. Please upload an MP4 file."}, status=400)
    
    try:
            # ques_id= ques_col.find_one({'qa_pairs.question_id': 'uuid'})
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        transcription_state = create_transcription_state(temp_file_path)

        given_ans = graph.invoke(transcription_state)
        os.unlink(temp_file_path)

        transcribed_text = given_ans.get('transcribed_text', [])

        if not transcribed_text:
            return Response({"error": "Transcription failed or no text found."}, status=500)


        return Response({"status": "success", "message": "Transcription successful.", "transcribed_text": transcribed_text})

    except Exception as e:
        if 'temp_file_path' in locals():
            try:
                os.unlink(temp_file_path)
            except:
                pass
        
        print(f"Error during transcription: {str(e)}")
        return Response({"error": f"An error occurred during transcription: {str(e)}"}, status=500)

    # for video_file, ques_id in zip(videos, ques_ids):
    #     try:
    #         ques_id= ques_col.find_one({'qa_pairs.question_id': 'uuid'})

    #         given_ans = graph.invoke({'start': 'transcribe_answer_node', 'video_file': video_file})

    #         transcribed_text = given_ans.get('transcribed_text', [])

    #         if not transcribed_text:
    #             return Response({"error": "Transcription failed or no text found."}, status=500)
            
    #         return Response({"status": "success", "message": "Transcription successful.", "transcribed_text": transcribed_text})
    #     except Exception as e:
    #         return Response({"error": f"An error occurred during transcription: {str(e)}"}, status=500)
    
