from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import ExtractedDataSerializer

from profiles.models import UserProfile
from .extractor import extract_all


class SkillExtractionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({"detail": "User profile not found"}, status=status.HTTP_404_NOT_FOUND)

        if not profile.pdf_text:
            return Response({"detail": "No PDF text found. Upload CV first."}, status=status.HTTP_400_BAD_REQUEST)

        extracted_data = extract_all(profile.pdf_text)

        serializer = ExtractedDataSerializer(extracted_data)
        return Response(serializer.data, status=status.HTTP_200_OK)
