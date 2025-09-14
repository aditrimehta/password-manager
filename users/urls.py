# users/urls.py
from django.urls import path
from .views import (
    SignupAPIView,
    VerifySignupOTPAPIView,
    LoginAPIView,
    VerifyLoginOTPAPIView,
)

urlpatterns = [
    path("signup/", SignupAPIView.as_view(), name="signup"),
    path("verify-signup-otp/", VerifySignupOTPAPIView.as_view(), name="verify-signup-otp"),
    path("login/", LoginAPIView.as_view(), name="login"),
    path("verify-login-otp/", VerifyLoginOTPAPIView.as_view(), name="verify-login-otp"),
]
