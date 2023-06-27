from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomBaseManager


class User(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    username = None
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=13)
    address = models.CharField(max_length=1000)
    is_organization = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    cus_id = models.CharField(
        max_length=200, null=True, unique=True
    )  # ? This may be used for Stripe accounts

    objects = CustomBaseManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    