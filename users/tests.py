from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from users.models import User, OTP # Ensure OTP is imported
from unittest.mock import patch
from datetime import timedelta
from django.utils import timezone

class UserAuthAPITestCase(APITestCase):

    def setUp(self):
        self.signup_url = reverse('signup')
        self.verify_signup_otp_url = reverse('verify_signup_otp')
        self.login_url = reverse('login')
        self.verify_login_otp_url = reverse('verify_login_otp')

        # Create a verified user for login tests
        self.verified_user_email = "verified@example.com"
        self.verified_user_password = "VerifiedPassword123"
        self.verified_user = User.objects.create_user(
            email=self.verified_user_email,
            password=self.verified_user_password
        )
        self.verified_user.is_verified = True
        self.verified_user.save()

    def tearDown(self):
        # Ensure client is logged out after each test
        self.client.logout()
        # Clean up any created users and OTPs to prevent interference,
        # although Django's test database teardown should handle most of this.
        # This can be useful for debugging if the test database isn't fully reset.
        User.objects.all().delete()
        OTP.objects.all().delete()
        super().tearDown()

    @patch('users.utils.send_otp') # Mock the send_otp function
    def test_signup_success(self, mock_send_otp):
        # Define a side effect for mock_send_otp that also creates the OTP object
        def mock_send_otp_side_effect(email_address):
            otp_code = "123456"
            OTP.objects.create(email=email_address, otp_code=otp_code)
            return otp_code
        mock_send_otp.side_effect = mock_send_otp_side_effect

        data = {
            "email": "newuser@example.com",
            "password": "NewUserPassword123"
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("OTP sent for verification", response.data['message'])
        self.assertTrue(User.objects.filter(email="newuser@example.com", is_verified=False).exists())
        self.assertTrue(OTP.objects.filter(email="newuser@example.com", otp_code="123456").exists())
        mock_send_otp.assert_called_once_with("newuser@example.com")

    @patch('users.utils.send_otp')
    def test_signup_existing_unverified_user_resends_otp(self, mock_send_otp):
        # Define a side effect for mock_send_otp that updates/creates the OTP object
        def mock_send_otp_side_effect(email_address):
            otp_code = "654321" # New OTP code
            # In a real scenario, your view logic should handle updating the OTP
            # For the test, we simulate that effect here directly if the utility does it
            OTP.objects.update_or_create(
                email=email_address,
                defaults={'otp_code': otp_code, 'created_at': timezone.now()}
            )
            return otp_code
        mock_send_otp.side_effect = mock_send_otp_side_effect

        # Create an unverified user first
        User.objects.create_user(email="unverified@example.com", password="password", is_verified=False)
        OTP.objects.create(email="unverified@example.com", otp_code="111111") # Original OTP

        data = {
            "email": "unverified@example.com",
            "password": "password"
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("OTP resent for verification", response.data['message'])
        # Now there should only be one OTP object, but its code should be updated
        self.assertEqual(OTP.objects.filter(email="unverified@example.com").count(), 1)
        self.assertTrue(OTP.objects.filter(email="unverified@example.com", otp_code="654321").exists())
        mock_send_otp.assert_called_once_with("unverified@example.com")

    def test_signup_existing_verified_user_fails(self):
        data = {
            "email": self.verified_user_email,
            "password": self.verified_user_password
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Assuming DRF serializer validation puts the error under 'email'
        # Or if your view explicitly returns a 'message' key for this case
        if 'message' in response.data:
            self.assertIn("Email already registered and verified", response.data['message'])
        elif 'email' in response.data:
            self.assertIn("Email already registered and verified", str(response.data['email'])) # Convert list to string for assertion
        else:
            self.fail(f"Unexpected response data structure: {response.data}")

        self.assertFalse(OTP.objects.filter(email=self.verified_user_email).exists()) # No new OTP sent

    def test_signup_invalid_data_fails(self):
        data = {
            "email": "invalid-email", # Invalid email format
            "password": "short"       # Too short password
        }
        response = self.client.post(self.signup_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("email", response.data)
        self.assertIn("password", response.data)

    def test_verify_signup_otp_success(self):
        user = User.objects.create_user(email="verify@example.com", password="password", is_verified=False)
        OTP.objects.create(email="verify@example.com", otp_code="112233")

        data = {
            "email": "verify@example.com",
            "otp": "112233"
        }
        response = self.client.post(self.verify_signup_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Account successfully verified", response.data['message'])
        self.assertTrue(User.objects.get(email="verify@example.com").is_verified)
        self.assertFalse(OTP.objects.filter(email="verify@example.com", otp_code="112233").exists()) # OTP deleted

    def test_verify_signup_otp_invalid_otp(self):
        user = User.objects.create_user(email="invalidotp@example.com", password="password", is_verified=False)
        OTP.objects.create(email="invalidotp@example.com", otp_code="111111")

        data = {
            "email": "invalidotp@example.com",
            "otp": "999999" # Incorrect OTP
        }
        response = self.client.post(self.verify_signup_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid OTP", response.data['message'])
        self.assertFalse(User.objects.get(email="invalidotp@example.com").is_verified)
        # OTP should still exist if it was just an invalid attempt, not expired
        self.assertTrue(OTP.objects.filter(email="invalidotp@example.com", otp_code="111111").exists())

    def test_verify_signup_otp_expired_otp(self):
        user = User.objects.create_user(email="expired@example.com", password="password", is_verified=False)
        # Create an OTP that is already expired
        expired_otp_obj = OTP.objects.create(email="expired@example.com", otp_code="000000")
        expired_otp_obj.created_at = timezone.now() - timedelta(minutes=15) # Assuming 10 min expiry
        expired_otp_obj.save()

        data = {
            "email": "expired@example.com",
            "otp": "000000"
        }
        response = self.client.post(self.verify_signup_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("OTP expired", response.data['message'])
        # Expecting both user and OTP to be deleted if OTP expired and user was unverified
        self.assertFalse(User.objects.filter(email="expired@example.com").exists())
        self.assertFalse(OTP.objects.filter(email="expired@example.com").exists())

    @patch('users.utils.send_otp')
    def test_login_success_sends_otp(self, mock_send_otp):
        def mock_send_otp_side_effect(email_address):
            otp_code = "987654"
            OTP.objects.create(email=email_address, otp_code=otp_code)
            return otp_code
        mock_send_otp.side_effect = mock_send_otp_side_effect

        data = {
            "email": self.verified_user_email,
            "password": self.verified_user_password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Login OTP sent", response.data['message'])
        self.assertTrue(OTP.objects.filter(email=self.verified_user_email, otp_code="987654").exists())
        mock_send_otp.assert_called_once_with(self.verified_user_email)

    def test_login_invalid_credentials_fails(self):
        data = {
            "email": self.verified_user_email,
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid credentials", response.data['message'])

    @patch('users.utils.send_otp')
    def test_login_unverified_user_resends_signup_otp(self, mock_send_otp):
        def mock_send_otp_side_effect(email_address):
            otp_code = "333333"
            # Update or create the OTP for the unverified user
            OTP.objects.update_or_create(
                email=email_address,
                defaults={'otp_code': otp_code, 'created_at': timezone.now()}
            )
            return otp_code
        mock_send_otp.side_effect = mock_send_otp_side_effect

        unverified_login_user = User.objects.create_user(email="unverified_login@example.com", password="password", is_verified=False)
        # Create an initial OTP for this unverified user to simulate it
        OTP.objects.create(email="unverified_login@example.com", otp_code="000000")

        data = {
            "email": "unverified_login@example.com",
            "password": "password"
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Account not verified. OTP resent for verification.", response.data['message'])
        self.assertEqual(OTP.objects.filter(email="unverified_login@example.com").count(), 1) # Only one OTP after resend
        self.assertTrue(OTP.objects.filter(email="unverified_login@example.com", otp_code="333333").exists())
        mock_send_otp.assert_called_once_with("unverified_login@example.com")

    def test_verify_login_otp_success(self):
        OTP.objects.create(email=self.verified_user_email, otp_code="445566")
        data = {
            "email": self.verified_user_email,
            "otp": "445566"
        }
        response = self.client.post(self.verify_login_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Login successful", response.data['message'])
        self.assertFalse(OTP.objects.filter(email=self.verified_user_email, otp_code="445566").exists()) # OTP deleted
        # Check if user is actually logged in (session)
        self.assertTrue('_auth_user_id' in self.client.session)
        self.assertEqual(int(self.client.session['_auth_user_id']), self.verified_user.id)

    def test_verify_login_otp_invalid_otp(self):
        OTP.objects.create(email=self.verified_user_email, otp_code="777777")
        data = {
            "email": self.verified_user_email,
            "otp": "888888" # Incorrect OTP
        }
        response = self.client.post(self.verify_login_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid OTP", response.data['message'])
        # OTP should still exist if it was just an invalid attempt, not expired
        self.assertTrue(OTP.objects.filter(email=self.verified_user_email, otp_code="777777").exists())

    def test_verify_login_otp_expired_otp(self):
        expired_otp_obj = OTP.objects.create(email=self.verified_user_email, otp_code="000000")
        expired_otp_obj.created_at = timezone.now() - timedelta(minutes=15)
        expired_otp_obj.save()

        data = {
            "email": self.verified_user_email,
            "otp": "000000"
        }
        response = self.client.post(self.verify_login_otp_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("OTP expired", response.data['message'])
        # Login OTPs are typically NOT deleted upon expiry unless your view explicitly does so
        # If your view *does* delete it, change this to assertFalse
        self.assertTrue(OTP.objects.filter(email=self.verified_user_email, otp_code="000000").exists())