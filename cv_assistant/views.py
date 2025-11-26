from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from profiles.models import UserProfile
from .ai_reasoning import generate_cv_assistant_output


# class CVAssistantView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         user = request.user
#         profile = UserProfile.objects.get(user=user)

#         if not profile or not profile.pdf_text:
#             return Response({"error": "No CV text found"}, status=400)

#         result = generate_cv_assistant_output(profile.pdf_text)

#         return Response({"cv_assistant": result})

import json
class CVAssistantView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.get(user=request.user)

        if not profile or not profile.pdf_text:
            return Response({"error": "No CV text found"}, status=400)

        raw_result = generate_cv_assistant_output(profile.pdf_text)

        # Try to parse JSON
        try:
            formatted = json.loads(raw_result)
        except json.JSONDecodeError:
            return Response({"error": "AI returned invalid JSON", "raw_output": raw_result}, status=500)

        return Response(formatted)
