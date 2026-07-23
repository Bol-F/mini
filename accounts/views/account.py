from django.contrib.auth import logout as django_logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.serializers.account import (
    AccountSerializer,
    AccountUpdateSerializer,
)


class AccountMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = AccountSerializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        serializer = AccountUpdateSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            AccountSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )

    def delete(self, request):
        account = request.user
        account.is_active = False
        account.save(update_fields=["is_active"])

        django_logout(request)

        return Response(
            {
                "message": "Account deleted successfully.",
            },
            status=status.HTTP_200_OK,
        )
