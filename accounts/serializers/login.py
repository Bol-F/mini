from rest_framework import serializers

from accounts.models import Account


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()

    password = serializers.CharField(
        write_only=True,
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs["email"].strip().lower()
        password = attrs["password"]

        account = Account.objects.filter(
            email__iexact=email,
        ).first()

        if account is None or not account.check_password(password):
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