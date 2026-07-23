from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from config.abstract_model_uuid_v7 import UUIDModel


class Account(UUIDModel, AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    is_email_verified = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email


class Profile(UUIDModel):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    picture = models.ImageField(upload_to="profile_pics/", blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.account.email}"


class EmailVerificationOTP(UUIDModel):
    account = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                   related_name="email_verification_otp")
    code_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    attempts = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"OTP for {self.account.email}"


# class AuthSession(UUIDModel):
#     account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="auth_sessions")
#     refresh_token_hash = models.CharField(max_length=255)
#     expires_at = models.DateTimeField()
#     revoked_at = models.DateTimeField(null=True, blank=True)
#
#     def __str__(self):
#         return f"Session of {self.account.email}"


class Role(UUIDModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Resource(UUIDModel):
    code = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class Action(UUIDModel):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.code


class AccessPermission(UUIDModel):
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name="access_permissions")
    action = models.ForeignKey(Action, on_delete=models.CASCADE, related_name="access_permissions")

    def __str__(self):
        return f"{self.resource.code}.{self.action.code}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["resource", "action"],
                name="unique_resource_action",
            )
        ]


class UserRole(UUIDModel):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_roles")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="user_roles")

    def __str__(self):
        return f"{self.account.email} - {self.role.name}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["account", "role"],
                name="unique_account_role",
            )
        ]


class RolePermission(UUIDModel):
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="role_permissions")
    permission = models.ForeignKey(AccessPermission, on_delete=models.CASCADE, related_name="role_permissions")

    def __str__(self):
        return f"{self.role.name} - {self.permission}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["role", "permission"],
                name="unique_role_permission",
            )
        ]
