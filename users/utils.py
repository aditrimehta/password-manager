from django.utils import timezone
from datetime import timedelta
import requests
import random
from django.conf import settings
from django.core.mail import send_mail

from users.models import OTP, User

def send_otp(email):
    otp = random.randint(100000, 999999)
    subject = "Your OTP Verification Code"
    message = f"Your OTP is {otp}. Do not share it with anyone."
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])
    return otp


def cleanup_unverified_users():
    expired_time = timezone.now() - timedelta(minutes=5)
    # Find unverified users whose latest OTP is expired
    expired_emails = OTP.objects.filter(created_at__lt=expired_time).values_list('email', flat=True)
    User.objects.filter(email__in=expired_emails, is_verified=False).delete()