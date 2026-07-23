from rest_framework import serializers

from accounts.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        source="account.email",
        read_only=True,
    )

    first_name = serializers.CharField(
        source="account.first_name",
        read_only=True,
    )

    last_name = serializers.CharField(
        source="account.last_name",
        read_only=True,
    )

    class Meta:
        model = Profile
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "picture",
            "date_of_birth",
        )
        read_only_fields = (
            "id",
            "email",
            "first_name",
            "last_name",
        )
