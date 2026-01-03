from rest_framework import serializers
from .models import QAPair
class QAPairSerializer(serializers.Serializer):
    question_id= serializers.CharField()
    question= serializers.CharField()
    answer= serializers.CharField()

class MongoQuestionPullSerializer(serializers.Serializer):
    id= serializers.CharField(source='_id')
    created_by = serializers.CharField()
    position = serializers.CharField()
    stack= serializers.CharField()
    level = serializers.CharField()
    qa_pairs = serializers.ListField(child=QAPairSerializer(),required=False, allow_null=True) 
    allowed_candidates = serializers.ListField(child=serializers.EmailField(), required=False)
    scheduled_time = serializers.DateTimeField(source="scheduled",required=False, allow_null=True)

class MongoQuestionSerializer(serializers.Serializer):
    question = serializers.CharField()

class CandidateAllSessionsSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id')
    position=serializers.CharField(required=False, allow_null=True, default=None)
    company= serializers.CharField(required=False, allow_null=True, default=None)
    scheduled_time = serializers.DateTimeField(source="scheduled",required=False, allow_null=True)    
class CandidateSessionsSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id')
    session_id = serializers.CharField()
    position= serializers.CharField(required=False, allow_null=True, default=None)
    company= serializers.CharField(required=False, allow_null=True, default=None)
    scheduled_time = serializers.DateTimeField(source="scheduled",required=False, allow_null=True)

class CandidateScoreSerializer(serializers.Serializer):
    question_id= serializers.CharField(required= False)
    ideal_answer= serializers.CharField(required=False, allow_null=True, default=None)
    given_answer = serializers.CharField(required= False)
    score = serializers.FloatField(required= False)

class CandidateResultSerializer(serializers.Serializer):
    id= serializers.CharField(source='_id')
    session_id = serializers.CharField()
    candidate_id = serializers.CharField()
    candidate_name = serializers.CharField()
    candidate_mail = serializers.EmailField()
    
    responses = CandidateScoreSerializer(many=True, required= False, allow_null=True)
    total_score = serializers.FloatField(required= False, allow_null= True)
    decision = serializers.CharField(required=False, allow_null=True)

    status = serializers.CharField()

class CandidateOwnResultSerializer(CandidateSessionsSerializer):
    decision = serializers.CharField(required=False, allow_null=True)
    status = serializers.CharField()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data.pop('scheduled_time', None)  
        return data


    