from django.urls import path, include
from .views import register_user, login_user

urlpatterns = [

    path('signup/', register_user, name="signup"),
    path('login/', login_user, name="login"),
]