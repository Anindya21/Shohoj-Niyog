from django.urls import path
from . import views

urlpatterns = [
    path('gen/', views.get_role_stacks_levels, name='get_role_stacks_levels'),
    path('add/', views.add_qa_pair, name='add_qa_pair'),
] 