# careerbot/views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import CareerBotRequestSerializer
from .prompts import build_career_prompt
from .services import ask_gemini
from profiles.models import UserProfile

class CareerBotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CareerBotRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        question = serializer.validated_data['question']
        profile = UserProfile.objects.get(user=request.user)

        prompt = build_career_prompt(profile, question)
        answer = ask_gemini(prompt)

        return Response({"answer": answer})
