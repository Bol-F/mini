from rest_framework import serializers

from accounts.services.otp import send_otp, verify_otp
from accounts.models import Account


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(
        min_length=6,
        max_length=6,
        write_only=True,
    )

    def validate_code(self, value):
        if not value.isdigit():
            raise serializers.ValidationError(
                "Code must contain only digits."
            )

        return value

    def create(self, validated_data):
        try:
            return verify_otp(
                email=validated_data["email"],
                code=validated_data["code"],
            )
        except ValueError as error:
            raise serializers.ValidationError(
                str(error)
            ) from error


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def create(self, validated_data):
        account = Account.objects.filter(
            email__iexact=validated_data["email"],
            is_active=True,
            is_email_verified=False,
        ).first()

        if account:
            send_otp(account)

        return validated_data