from rest_framework import serializers
from .models import QAPair
class QAPairSerializer(serializers.Serializer):
    question_id= serializers.CharField()
    question= serializers.CharField()
    answer= serializers.CharField()

class MongoQuestionPullSerializer(serializers.Serializer):
    id= serializers.CharField(source='_id')
    created_by = serializers.CharField(),
    position = serializers.CharField()
    stack= serializers.CharField()
    level = serializers.CharField()
    qa_pairs = serializers.ListField(child=QAPairSerializer()) 
    allowed_candidates = serializers.ListField(child=serializers.EmailField(), required=False)
    scheduled_time = serializers.DateTimeField(source="scheduled",required=False, allow_null=True)

class MongoQuestionSerializer(serializers.Serializer):
    question = serializers.CharField()


class CandidateSessionsSerializer(serializers.Serializer):
    session_id = serializers.CharField(source='_id')
    position= serializers.CharField(required=False, allow_null=True, default=None)

class CandidateScoreSerializer(serializers.Serializer):
    question_id= serializers.CharField()
    given_answer = serializers.CharField()
    score = serializers.FloatField()
class CandidateResultSerializer(serializers.Serializer):
    id= serializers.CharField(source='_id')
    session_id = serializers.CharField()
    candidate_id = serializers.CharField()
    candidate_name = serializers.CharField()
    candidate_mail = serializers.EmailField()
    responses = serializers.ListField(child=CandidateScoreSerializer())
    total_score = serializers.FloatField()
    decision = serializers.CharField()

class CandidateOwnResultSerializer(CandidateSessionsSerializer):
    decision = serializers.CharField()





# class VideoSerializer(serializers.Serializer):
#     video_file= serializers.FileField(upload_to ='res/')


# class TranscriptionSerializer(serializers.Serializer):
#     video_files = serializers.ListField(child=VideoSerializer())
#     trnscribed_text= serializers.ListField(child=serializers.CharField())
#     session_id = serializers.CharField()
#     candidate_id = serializers.CharField()

    