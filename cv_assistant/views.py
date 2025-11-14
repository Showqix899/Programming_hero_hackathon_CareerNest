from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from profiles.models import UserProfile
from .ai_reasoning import generate_cv_assistant_output


class CVAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        if not profile or not profile.pdf_text:
            return Response({"error": "No CV text found"}, status=400)

        result = generate_cv_assistant_output(profile.pdf_text)

        return Response({"cv_assistant": result})
