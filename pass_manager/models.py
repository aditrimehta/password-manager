from django.db import models
from django.conf import settings
from cryptography.fernet import Fernet


def get_cipher():
    return Fernet(settings.FERNET_KEY)


class VaultItem(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="vault_items"
    )
    website = models.CharField(max_length=255)
    username = models.BinaryField()             # stored encrypted
    password = models.BinaryField()             # stored encrypted
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_credentials(self, username, password):
        """Encrypt before saving"""
        cipher = get_cipher()
        self.username = cipher.encrypt(username.encode())
        self.password = cipher.encrypt(password.encode())

    def get_credentials(self):
        """Decrypt for display"""
        cipher = get_cipher()
        return {
            "username": cipher.decrypt(bytes(self.username)).decode(),
            "password": cipher.decrypt(bytes(self.password)).decode(),
        }

    def __str__(self):
        return f"{self.website} ({self.user.phonenumber})"
