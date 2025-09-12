from django.http import JsonResponse
from django.shortcuts import render

from users.models import OTP, User
from users.utils import cleanup_unverified_users, send_otp

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model, authenticate, login
# Create your views here.
@csrf_exempt
def signup_view(request):
    cleanup_unverified_users()
    email = request.POST.get("email")
    password = request.POST.get("password")

    user = User.objects.filter(email=email).first()
    if user:
        if not user.is_verified:
            otp = send_otp(email)
            OTP.objects.create(email=email, otp_code=str(otp))
            return JsonResponse({"status": "success", "message": "OTP resent for verification"})
        return JsonResponse({"status": "error", "message": "email already registered"})


    user = User.objects.create_user(email=email, password=password)
    user.is_verified = False
    user.save()

    otp = send_otp(email)
    OTP.objects.create(email=email, otp_code=str(otp))

    return JsonResponse({"status": "success", "message": "OTP sent for verification"})
@csrf_exempt
def verify_signup_otp_view(request):
    email = request.POST.get("email")
    entered_otp = request.POST.get("otp")

    try:
        otp_obj = OTP.objects.filter(email=email).latest('created_at')
    except OTP.DoesNotExist:
        return JsonResponse({"status": "error", "message": "No OTP found"})

    if otp_obj.is_expired():
        # Delete unverified user
        try:
            user = User.objects.get(email=email, is_verified=False)
            user.delete()
        except User.DoesNotExist:
            pass  # User might have been deleted already
        return JsonResponse({"status": "error", "message": "OTP expired. Please signup again."})

    if otp_obj.otp_code == entered_otp:
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()
        return JsonResponse({"status": "success", "message": "Signup verified"})
    else:
        return JsonResponse({"status": "error", "message": "Invalid OTP"})

@csrf_exempt
def login_view(request):
    email = request.POST.get("email")
    password = request.POST.get("password")

    user = authenticate(request, email=email, password=password)

    if user is None:
        return JsonResponse({"status": "error", "message": "Invalid credentials"})

    if not user.is_verified:
        return JsonResponse({"status": "error", "message": "User not verified"})

    otp = send_otp(email)
    OTP.objects.create(email=email, otp_code=str(otp))

    return JsonResponse({"status": "success", "message": "OTP sent for login"})
@csrf_exempt
def verify_login_otp_view(request): 
    email = request.POST.get("email") 
    entered_otp = request.POST.get("otp") 
    try: 
        otp_obj = OTP.objects.filter(email=email).latest('created_at') 
    except  OTP.DoesNotExist: 
        return JsonResponse({"status": "error", "message": "No OTP found"}) 
    if otp_obj.is_expired(): 
        return JsonResponse({"status": "error", "message": "OTP expired"}) 
    if otp_obj.otp_code == entered_otp: 
        user = User.objects.get(email=email) 
        login(request, user) 
        return JsonResponse({"status": "success", "message": "Login successful"}) 
    else: 
        return JsonResponse({"status": "error", "message": "Invalid OTP"}) 