from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.register import RegisterSerializer
from accounts.services.otp import send_otp


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.save()
        send_otp(account)

        return Response(
            {
                "message": "Account created. OTP was sent.",
                "email": account.email,
            },
            status=status.HTTP_201_CREATED,
        )
    