from .models import CustomUser
from rest_framework import serializers


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'phone', 'role', 'company']


    def validate(self,data):
        role= data.get('role')

        if role=='interviewer' and not data.get('company'):
            raise serializers.ValidationError({"company": " Company is required for interviewers."})
        
        elif role=='candidate' and data.get('company'):
            raise serializers.ValidationError({"company":" Company should not be set for candidates."})
        
        elif role not in ['interviewer','candidate']:
            raise serializers.ValidationError({"role": " Role must be either 'interviewer' or 'candidate'."})
        
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(

            username = validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone'],
            role=validated_data['role'],
            company= validated_data['company']
        )

        return user

    