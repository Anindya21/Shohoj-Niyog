from rest_framework import serializers
from .models import QAPair
class QAPairSerializer(serializers.Serializer):
    question_id= serializers.CharField()
    question= serializers.CharField()
    answer= serializers.CharField()

class MongoQuestionPullSerializer(serializers.Serializer):
    id= serializers.CharField(source='_id')
    position = serializers.CharField()
    stack= serializers.CharField()
    level = serializers.CharField()
    qa_pairs = serializers.ListField(child=QAPairSerializer()) 
    allowed_candidates = serializers.ListField(child=serializers.EmailField(), required=False)

class MongoQuestionSerializer(serializers.Serializer):
    question = serializers.CharField()


# class VideoSerializer(serializers.Serializer):
#     video_file= serializers.FileField(upload_to ='res/')


# class TranscriptionSerializer(serializers.Serializer):
#     video_files = serializers.ListField(child=VideoSerializer())
#     trnscribed_text= serializers.ListField(child=serializers.CharField())
#     session_id = serializers.CharField()
#     candidate_id = serializers.CharField()

    