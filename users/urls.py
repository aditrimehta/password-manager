# users/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('verify-signup-otp/', views.verify_signup_otp_view, name='verify_signup_otp'),
    path('login/', views.login_view, name='login'),
    path('verify-login-otp/', views.verify_login_otp_view, name='verify_login_otp'),
]
