from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import CustomUser

# Create your views here.

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data= request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    username= request.data.get("username")
    password= request.data.get("password")

    user= authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh":str(refresh),
            "username": user.username
            })
    else:
        return Response({"detail":"Invalid Credential"}, status=status.HTTP_401_UNAUTHORIZED)
    