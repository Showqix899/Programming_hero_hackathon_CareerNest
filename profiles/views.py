from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserProfileSerializer
from .models import UserProfile
import pdfplumber

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            profile.email=request.user.email
            profile.save()
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found ."}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)

            # Use pdfplumber to extract text
            text = ""
            pdf_path = profile.cv_pdf.path  # IMPORTANT

            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
                    else:
                        text += "[NO TEXT FOUND ON PAGE]\n"

            profile.pdf_text = text
            profile.email = request.user.email
            profile.save()

        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)