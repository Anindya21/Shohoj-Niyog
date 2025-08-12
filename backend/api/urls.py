from django.urls import path, include
from . import views

urlpatterns = [
    path('gen/', views.get_role_stacks_levels, name='generate_qa_pairs'),
    path('findall/', views.get_allqa, name='GetAllQA'),
    path('find/<str:requested_id>', views.get_single_question, name="Get Single Question"),
    path('val/', views.validate_candidate, name= "Authorization for Interview Access"),
    path('response/', views.user_response, name="Save Candidate Response"),
    
] 
