from django.urls import path, include
from .views import register_user, login_user, forgot_password, reset_password

urlpatterns = [

    path('signup/', register_user, name="signup"),
    path('login/', login_user, name="login"),
    path('auth/forgot-password/', forgot_password, name="forgot-password"),
    path('auth/reset-password/', reset_password, name="reset-password"),
]