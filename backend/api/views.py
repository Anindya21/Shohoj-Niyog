from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import QAPair
from .serializers import QAPairSerializer
from .mongo import get_db_handle
from graph.builder import build_graph
from utils.env_loader import load_env
import os 
import time

load_env()

@api_view(['POST'])
def add_qa_pair(request):
    serializer = QAPairSerializer(data= request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)

@api_view(["POST"])
def get_role_stacks_levels(request):
    # timing = {}
    role = request.data.get('role')
    stacks = request.data.get('stacks')
    level = request.data.get('level')

    if not role or not stacks or not level:
        return Response({"error": "role, stacks, and level are required."}, status=400)
    
    t0= time.time()
    graph= build_graph()
    t1 = time.time()
    
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

    for qa in result["question_answer_pairs"]:
        question = qa['question']
        answer = qa['answer']
        collection.insert_one({"role": role,"stack":stacks, "level":level ,"question": question, "answer": answer})    
    
    # t5 = time.time()
    # timing['Data Insertion Time into Database'] = t5 - t4
    # print("Timing:", timing)
    return Response({"status": "success", "message": "Questions and answers generated and saved."})

# @api_view(['GET'])
