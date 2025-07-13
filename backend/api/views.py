from rest_framework.response import Response
from rest_framework.decorators import api_view
from base.models import QAPair
from .serializers import QAPairSerializer
# from backend.mongo import get_db_handle

@api_view(['GET'])
def get_qa_pairs(request):

    qa_pairs = QAPair.objects.all()
    serializer = QAPairSerializer(qa_pairs, many=True)
    
    return Response(serializer.data)


@api_view(['POST'])
def add_qa_pair(request):
    serializer = QAPairSerializer(data= request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)