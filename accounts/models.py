from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.abstract_model_uuid_v7 import UUIDModel


class Account(UUIDModel, AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.email


class Profile(UUIDModel):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    picture = models.ImageField(upload_to="profile_pics/", blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.account.email}"

class EmailVerificationOTP(UUIDModel):
    account = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="email_verification_otp",
    )
    code_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"OTP for {self.account.email}"