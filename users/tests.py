from django.test import TestCase, Client
from django.urls import reverse
from users.models import User, OTP

class EmailOTPFlowTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.email = "testuser@example.com"
        self.password = "TestPassword123"

    def test_signup_and_login_email_otp(self):
        # --------- SIGNUP STEP ---------
        response = self.client.post(reverse('signup'), {
            'email': self.email,
            'password': self.password
        })
        print("Signup Response:", response.json())
        self.assertEqual(response.status_code, 200)

        # --------- FETCH OTP FROM DB FOR SIGNUP ---------
        otp_obj = OTP.objects.filter(email=self.email).latest('created_at')
        signup_otp = otp_obj.otp_code

        # --------- VERIFY SIGNUP OTP ---------
        response = self.client.post(reverse('verify_signup_otp'), {
            'email': self.email,
            'otp': signup_otp
        })
        print("Verify Signup OTP Response:", response.json())
        self.assertEqual(response.status_code, 200)

        # --------- LOGIN STEP ---------
        response = self.client.post(reverse('login'), {
            'email': self.email,
            'password': self.password
        })
        print("Login Response:", response.json())
        self.assertEqual(response.status_code, 200)

        # --------- FETCH OTP FROM DB FOR LOGIN ---------
        otp_obj = OTP.objects.filter(email=self.email).latest('created_at')
        login_otp = otp_obj.otp_code

        # --------- VERIFY LOGIN OTP ---------
        response = self.client.post(reverse('verify_login_otp'), {
            'email': self.email,
            'otp': login_otp
        })
        print("Verify Login OTP Response:", response.json())
        self.assertEqual(response.status_code, 200)

        # --------- FINAL CHECK ---------
        user = User.objects.get(email=self.email)
        self.assertTrue(user.is_verified)
