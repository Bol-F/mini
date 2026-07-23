from django.contrib.auth import logout as django_logout
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        django_logout(request)

        return Response(
            {
                "message": "Logout successful.",
            },
            status=status.HTTP_200_OK,
        )
