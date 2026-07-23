from rest_framework import serializers

from accounts.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_email_verified",
            "date_joined",
        )
        read_only_fields = fields


class AccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            "first_name",
            "last_name",
        )
