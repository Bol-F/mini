from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.otp import (
    ResendOTPSerializer,
    VerifyOTPSerializer,
)


class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.save()

        return Response(
            {
                "message": "Email verified successfully.",
                "email": account.email,
            },
            status=status.HTTP_200_OK,
        )


class ResendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResendOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": (
                    "If the account exists and is not verified, "
                    "a new OTP was sent."
                )
            },
            status=status.HTTP_200_OK,
        )
