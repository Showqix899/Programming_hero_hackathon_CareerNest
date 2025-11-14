from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from profiles.models import UserProfile
from .extractor import extract_all


class SkillExtractionView(APIView):
    """
    Extract skills, tools, and roles from a user's profile (cv_text field).
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.profile
        except UserProfile.DoesNotExist:
            return Response(
                {"detail": "User profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        text_to_extract = profile.cv_text or ""
        if not text_to_extract:
            return Response(
                {"detail": "No text found in user's profile for extraction."},
                status=status.HTTP_400_BAD_REQUEST
            )

        extracted_data = extract_all(text_to_extract)

        return Response(
            {
                "user": profile.user.email or str(profile.user),
                "skills": extracted_data.get("skills", []),
                "tools": extracted_data.get("tools", []),
                "roles": extracted_data.get("roles", []),
                "nlp_entities": extracted_data.get("nlp_entities", []),
            },
            status=status.HTTP_200_OK
        )
