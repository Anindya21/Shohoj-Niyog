from rest_framework import serializers
from base.models import QAPair

class QAPairSerializer(serializers.Serializer):
    question= serializers.CharField()
    answer= serializers.CharField()

class MongoQuestionPullSerializer(serializers.Serializer):
    id= serializers.CharField(source='_id')
    role = serializers.CharField()
    stack= serializers.CharField()
    level = serializers.CharField()
    qa_pairs = QAPairSerializer(many=True)