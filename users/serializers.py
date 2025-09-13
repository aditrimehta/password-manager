# users/serializers.py
from rest_framework import serializers
from users.models import User, OTP # Assuming User and OTP models are in users.models

class UserSignupSerializer(serializers.Serializer):
    """
    Serializer for user registration input.
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    def validate_email(self, value):
        # Custom validation to check if email is already registered and verified
        if User.objects.filter(email=value, is_verified=True).exists():
            raise serializers.ValidationError("This email is already registered and verified.")
        return value

class OTPSendSerializer(serializers.Serializer):
    """
    Serializer for sending OTP (e.g., for login or resending signup OTP).
    """
    email = serializers.EmailField(required=True)

class OTPVerifySerializer(serializers.Serializer):
    """
    Serializer for verifying an OTP.
    """
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True, min_length=6, max_length=6) # Assuming 6-digit OTP

class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login input (email and password).
    """
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)