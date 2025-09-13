# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('verify-signup-otp/', views.VerifySignupOTPAPIView.as_view(), name='verify_signup_otp'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('verify-login-otp/', views.VerifyLoginOTPAPIView.as_view(), name='verify_login_otp'),
]