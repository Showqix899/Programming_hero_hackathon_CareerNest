from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from profiles.models import UserProfile
from .extractor import extract_all


class SkillExtractionView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        profile = request.user.profile  # already auth, no need try/except

        text_to_extract = " ".join(profile.pdf_text)
        if not text_to_extract:
            return Response({"detail": "No CV text found."}, status=status.HTTP_400_BAD_REQUEST)

        extracted_data = extract_all(text_to_extract)

        return Response({
            "user": profile.user.email,
            "skills_found": extracted_data.get("skills_found", {}),
            "tools_found": extracted_data.get("tools_found", {}),
            "roles_found": extracted_data.get("roles_found", {}),
            "confidence_score": extracted_data.get("confidence_score", 0),
        }, status=status.HTTP_200_OK)
