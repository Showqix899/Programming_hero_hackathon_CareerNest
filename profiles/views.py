from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
# Assuming these are defined in your project
from .serializers import UserProfileSerializer
from .models import UserProfile
import pdfplumber
import PyPDF2
from .utils import fix_broken_words

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            profile.email = request.user.email  # keep email updated
            profile.save()
        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        li=[]
        try:
            profile = UserProfile.objects.get(user=request.user)

            #  Check if a CV is uploaded in request
            uploaded_pdf = request.FILES.get("cv_pdf", None)

            if uploaded_pdf:
                try:
                    # Read PDF from memory (NOT FROM DISK ❌)
                    reader = PyPDF2.PdfReader(uploaded_pdf)

                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            for line in extracted.split("\n"):
                                clean_line = line.strip()
                                fixed_word =fix_broken_words(clean_line)
                                li.append(fixed_word.lower())
                        else:
                            pass
                    if  not li:
                            return Response({"error:","can not extract the pdf"})
                    profile.pdf_text = li
                    profile.save()

                except Exception as e:
                    return Response(
                        {"error": f"Error processing PDF: {str(e)}"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                print("No new CV uploaded.")
            
            profile.email = request.user.email
            profile.save()

        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)

        # Save other fields through serializer
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
