from django.contrib.auth import login as django_login
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.account import AccountSerializer
from accounts.serializers.login import LoginSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        account = serializer.validated_data["account"]

        django_login(
            request,
            account,
            backend="django.contrib.auth.backends.ModelBackend",
        )

        return Response(
            {
                "message": "Login successful.",
                "account": AccountSerializer(account).data,
            },
            status=status.HTTP_200_OK,
        )
    