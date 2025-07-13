from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_qa_pairs),
    path('add/', views.add_qa_pair),
] 