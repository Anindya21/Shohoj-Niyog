from django.urls import path
from . import views

urlpatterns = [
    path('gen/', views.get_role_stacks_levels, name='generate_qa_pairs'),
    path('find/', views.get_question, name='get_question'),
] 