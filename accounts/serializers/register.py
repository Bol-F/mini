import uuid

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers

from accounts.models import Account, Profile
from accounts.services.otp import create_and_send_email_otp


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    password2 = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    class Meta:
        model = Account
        fields = (
            "email",
            "first_name",
            "last_name",
            "password",
            "password2",
        )

    def validate_email(self, value):
        email = value.strip().lower()

        if Account.objects.filter(email__iexact=email).exists():
            raise serializers.ValidationError(
                "An account with this email already exists."
            )

        return email

    def validate(self, attrs):
        password = attrs["password"]
        password2 = attrs["password2"]

        if password != password2:
            raise serializers.ValidationError(
                {
                    "password2": "Passwords do not match.",
                }
            )

        temporary_account = Account(
            email=attrs["email"],
            first_name=attrs.get("first_name", ""),
            last_name=attrs.get("last_name", ""),
        )

        try:
            validate_password(
                password,
                user=temporary_account,
            )
        except DjangoValidationError as error:
            raise serializers.ValidationError(
                {
                    "password": list(error.messages),
                }
            ) from error

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password2")

        internal_username = f"user_{uuid.uuid7().hex}"

        with transaction.atomic():
            account = Account.objects.create_user(
                username=internal_username,
                password=password,
                is_email_verified=False,
                **validated_data,
            )

            Profile.objects.create(account=account)

            transaction.on_commit(
                lambda: create_and_send_email_otp(account)
            )

        return account