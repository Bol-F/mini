from rest_framework import serializers

from accounts.models import Account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate_email(self, value):
        return value.strip().lower()

    def validate(self, attrs):
        account = Account.objects.filter(
            email__iexact=attrs["email"],
        ).first()

        if account is None:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not account.check_password(attrs["password"]):
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not account.is_active:
            raise serializers.ValidationError(
                "Invalid email or password."
            )

        if not account.is_email_verified:
            raise serializers.ValidationError(
                {
                    "email": "Verify your email before login.",
                }
            )

        attrs["account"] = account
        return attrs