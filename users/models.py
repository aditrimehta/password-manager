from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, phonenumber, password=None, **extra_fields):
        if not phonenumber:
            raise ValueError('The phone number field must be set')
        user = self.model(phonenumber=phonenumber, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, phonenumber, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phonenumber, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phonenumber = models.CharField(max_length=10, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified=models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = 'phonenumber'
    REQUIRED_FIELDS = []    