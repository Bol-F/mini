from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.abstract_model_uuid_v7 import UUIDModel


class Account(UUIDModel, AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        MODERATOR = "moderator", "Moderator"
        USER = "user", "User"

    email = models.EmailField(max_length=255, unique=True)
    is_email_verified = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
    )
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self.role = self.Role.ADMIN

            update_fields = kwargs.get("update_fields")
            if update_fields is not None:
                kwargs["update_fields"] = set(update_fields) | {"role"}

        super().save(*args, **kwargs)


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
