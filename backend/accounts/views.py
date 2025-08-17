from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer
from .models import CustomUser
from logics.db.mongo import get_db_handle
import os
# Create your views here.

@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data= request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    email= request.data.get("email")
    
    user= serializer.save()

    print(user.id)

    if user.role =="interviewer":
        return Response({"message": "Interviewer registered successfully!"}, status=status.HTTP_201_CREATED)

    uri = os.getenv("mongo_uri")
    db, _ = get_db_handle("interview_db")
    collection = db['qa_pairs']

    sessions_with_email = list(collection.find({"allowed_candidates": email}))
    
    print(f"Found {len(sessions_with_email)} sessions for this candidate")
    
    if not sessions_with_email:
        return Response({
            "message": "Candidate registered successfully!",
            "sessions_found": 0,
            "note": "No interview sessions assigned to this email"
        }, status=status.HTTP_201_CREATED)

    # Replace email with user_id in each session
    updated_sessions = 0
    session_details = []
    
    for session in sessions_with_email:
        session_id = session['_id']
        current_candidates = session['allowed_candidates']
        
        # Replace the email with user_id in the candidates list
        updated_candidates = [
            str(user.id) if candidate == email else candidate 
            for candidate in current_candidates
        ]
        
        # Update the session with new candidates list
        result = collection.update_one(
            {"_id": session_id},
            {"$set": {"allowed_candidates": updated_candidates}}
        )
        
        if result.modified_count > 0:
            updated_sessions += 1
            print(f"Updated session {session_id}")
            
            # Collect session info for response
            session_details.append({
                "session_id": str(session_id)
            })
        else:
            print(f"Failed to update session {session_id}")
    
    print(f"Successfully updated {updated_sessions} sessions")
    
    return Response({
        "message": "Candidate registered successfully!",
        "sessions_found": len(sessions_with_email),
        "candidate_id": str(user.id),
        "assigned_sessions": session_details
    }, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_user(request):
    email= request.data.get("email")
    password= request.data.get("password")

    user= authenticate(email=email, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
    
        return Response({
            "access": str(refresh.access_token),
            "refresh":str(refresh),
            "username": user.username,
            "role": user.role,
            "user_id": user.id
            })
    else:
        return Response({"detail":"Invalid Credential"}, status=status.HTTP_401_UNAUTHORIZED)
    

