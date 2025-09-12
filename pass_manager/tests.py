from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import VaultItem
from django.conf import settings
from cryptography.fernet import Fernet

User = get_user_model()


class VaultItemAPITest(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(phonenumber="9876543210", password="testpass", is_verified=True)
        self.client.login(username="9876543210", password="testpass")  # session auth
        self.cipher = Fernet(settings.FERNET_KEY)
        self.vault_url = reverse("vault-list")  # DRF router name for list/create

    def test_crud_vault_item(self):
        # --- CREATE ---
        data = {
            "website": "facebook.com",
            "username": "alice123",
            "password": "supersecret"
        }
        response = self.client.post(self.vault_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        item_id = response.data["id"]

        # --- READ / LIST ---
        response = self.client.get(self.vault_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["decrypted_username"], "alice123")
        self.assertEqual(response.data[0]["decrypted_password"], "supersecret")

        # --- UPDATE ---
        update_data = {
            "website": "facebook.com",
            "username": "alice456",
            "password": "newsecret"
        }
        response = self.client.patch(f"{self.vault_url}{item_id}/", update_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["decrypted_username"], "alice456")
        self.assertEqual(response.data["decrypted_password"], "newsecret")

        # --- DELETE ---
        response = self.client.delete(f"{self.vault_url}{item_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(VaultItem.objects.filter(user=self.user).count(), 0)
