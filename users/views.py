# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

from users.models import OTP, User
from users.utils import cleanup_unverified_users, send_otp
from users.serializers import (
    UserSignupSerializer,
    OTPVerifySerializer,
    UserLoginSerializer,
)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


# ---------------- Signup ---------------- #
class SignupAPIView(APIView):
    def post(self, request):
        cleanup_unverified_users()
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = User.objects.filter(email=email).first()

            if user:
                if not user.is_verified:
                    # User exists but not verified, resend OTP
                    otp = send_otp(email)
                    OTP.objects.create(email=email, otp_code=str(otp))
                    return Response(
                        {
                            "status": "success",
                            "message": "OTP resent for verification. Please verify your account.",
                        },
                        status=status.HTTP_200_OK,
                    )
                return Response(
                    {
                        "status": "error",
                        "message": "Email already registered and verified.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Create new unverified user
            user = User.objects.create_user(email=email, password=password)
            user.is_verified = False
            user.save()

            otp = send_otp(email)
            OTP.objects.create(email=email, otp_code=str(otp))

            return Response(
                {
                    "status": "success",
                    "message": "Account created. OTP sent for verification.",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifySignupOTPAPIView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            entered_otp = serializer.validated_data["otp"]

            try:
                otp_obj = OTP.objects.filter(email=email).latest("created_at")
            except OTP.DoesNotExist:
                return Response(
                    {"status": "error", "message": "No OTP found for this email."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if otp_obj.is_expired():
                try:
                    user = User.objects.get(email=email, is_verified=False)
                    user.delete()
                except User.DoesNotExist:
                    pass
                return Response(
                    {
                        "status": "error",
                        "message": "OTP expired. Please sign up again to get a new OTP.",
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if otp_obj.otp_code == entered_otp:
                try:
                    user = User.objects.get(email=email, is_verified=False)
                    user.is_verified = True
                    user.save()
                    otp_obj.delete()

                    # ✅ Auto-login after signup
                    tokens = get_tokens_for_user(user)

                    return Response(
                        {
                            "status": "success",
                            "message": "Account successfully verified.",
                            "tokens": tokens,
                        },
                        status=status.HTTP_200_OK,
                    )
                except User.DoesNotExist:
                    return Response(
                        {
                            "status": "error",
                            "message": "User not found or already verified.",
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"status": "error", "message": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------- Login ---------------- #
class LoginAPIView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]

            user = authenticate(request, email=email, password=password)

            if user is None:
                return Response(
                    {"status": "error", "message": "Invalid credentials."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if not user.is_verified:
                otp = send_otp(email)
                OTP.objects.create(email=email, otp_code=str(otp))
                return Response(
                    {
                        "status": "error",
                        "message": "Account not verified. OTP resent for verification.",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )

            # Verified → send login OTP
            otp = send_otp(email)
            OTP.objects.create(email=email, otp_code=str(otp))

            return Response(
                {"status": "success", "message": "Login OTP sent to your email."},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyLoginOTPAPIView(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            entered_otp = serializer.validated_data["otp"]

            try:
                otp_obj = OTP.objects.filter(email=email).latest("created_at")
            except OTP.DoesNotExist:
                return Response(
                    {"status": "error", "message": "No OTP found for this email."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if otp_obj.is_expired():
                return Response(
                    {"status": "error", "message": "OTP expired. Please request a new login OTP."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if otp_obj.otp_code == entered_otp:
                try:
                    user = User.objects.get(email=email, is_verified=True)
                    login(request, user)
                    otp_obj.delete()

                    # ✅ Issue JWT tokens on login success
                    tokens = get_tokens_for_user(user)

                    return Response(
                        {
                            "status": "success",
                            "message": "Login successful.",
                            "tokens": tokens,
                        },
                        status=status.HTTP_200_OK,
                    )
                except User.DoesNotExist:
                    return Response(
                        {"status": "error", "message": "User not found or not verified."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            return Response(
                {"status": "error", "message": "Invalid OTP."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
