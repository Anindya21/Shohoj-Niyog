from rest_framework import serializers
from base.models import QAPair

class QAPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = QAPair
        fields = ['id', 'question', 'answer', 'created']
        # read_only_fields = ['id', 'created']