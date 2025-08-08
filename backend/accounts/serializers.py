from .models import CustomUser
from rest_framework import serializers
import uuid

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone', 'role']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(

            username = validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            role=validated_data['role']
        )

        return user

    