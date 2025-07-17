from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import QAPair
from .serializers import MongoQuestionPullSerializer, MongoQuestionSerializer
from .mongo import get_db_handle
from graph.builder import build_graph
from utils.env_loader import load_env
import os 
from bson import ObjectId

load_env()

@api_view(["POST"])
def get_role_stacks_levels(request):
    # timing = {}
    role = request.data.get('role')
    stacks = request.data.get('stacks')
    level = request.data.get('level')

    if not role or not stacks or not level:
        return Response({"error": "role, stacks, and level are required."}, status=400)
    
    # t0= time.time()
    graph= build_graph()
    # t1 = time.time()
    
    # timing['Graph Building'] = t1 - t0
    
    inputs = {
        "role": role,
        "stacks": stacks,
        "level": level  
    }
    
    # t2 = time.time()
    result = graph.invoke(inputs)
    # t3 = time.time()

    # timing['QA Generation Time'] = t3 - t2

    uri = os.getenv("mongo_uri")

    # timing["Mongo Connection"] = time.time() - t3

    print(result)

    # t4 = time.time()
    db, _ = get_db_handle("interview_db")

    collection = db['qa_pairs']

    qa_pairs = []
    
    for qa in result["question_answer_pairs"]:
        question = qa['question']
        answer = qa['answer']
        qa_pairs.append({'question': question, 'answer': answer})

    inserted_rec= collection.insert_one({"role": role,"stack":stacks, "level":level ,'qa_pairs': qa_pairs})    
        
    # t5 = time.time()
    # timing['Data Insertion Time into Database'] = t5 - t4
    # print("Timing:", timing)

    ID= str(inserted_rec.inserted_id)
    return Response({"status": "success", "message": "Questions and answers generated and saved.", "Session_ID": f"{ID}"})

@api_view(['GET'])
def get_allqa(request):
    # role= request.GET.get('role')
    uri = os.getenv("mongo_uri")
    
    # if not role:
    #     return Response({"error": "Role parameter is required."}, status=400)
    
    db, _ = get_db_handle("interview_db")
    collection = db['qa_pairs']

    # doc= collection.find_one({'role': role})
    docs= list(collection.find())
    # if not doc:
    #     return Response({"error": "No question found for the specified role."}, status=404)
    
    # docs['_id'] = str(docs['_id'])
    # serialized_docs = []
    for doc in docs:
        doc['_id'] = str(doc['_id'])
        # serialized_docs.append(doc)
    
    serializer = MongoQuestionPullSerializer(docs, many=True)
    
    return Response(serializer.data)

### GET individual interview by session ID
### in POST I want a session ID in response to be created and returned (Question ID)
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







