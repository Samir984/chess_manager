import secrets
import uuid
from typing import Any

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.db import models

from .validator import validate_file_size


def get_default_token():
    return secrets.token_hex(20)


# Custom User Manager
class CustomerUserManager(BaseUserManager): # type: ignore
    def create_user(self, email:str, password=None, **extra_fields:Any): # type: ignore
        if not email:
            raise ValueError("The Email field must be set ")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields) # type: ignore
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email:str, password=None, **extra_fields:Any): # type: ignore
        print("Create superuser custome manager running\n\n\n\n")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        return self.create_user(email, password, **extra_fields) # type: ignore


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    email = models.EmailField(unique=True)
    image = models.URLField(null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomerUserManager() # type: ignore

    def __str__(self):
        return self.get_full_name()


class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(
        upload_to="report/", validators=[validate_file_size]
    )
    created_at = models.DateTimeField(auto_now_add=True)


class Token(models.Model):
    key = models.CharField(
        max_length=255, unique=True, default=get_default_token
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Token for {self.user}"
