from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Profile
from accounts.serializers.profile import ProfileSerializer


class ProfileMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get_profile(self, account):
        profile, _ = Profile.objects.get_or_create(
            account=account,
        )
        return profile

    def get(self, request):
        profile = self.get_profile(request.user)
        serializer = ProfileSerializer(profile)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def patch(self, request):
        profile = self.get_profile(request.user)

        serializer = ProfileSerializer(
            profile,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )