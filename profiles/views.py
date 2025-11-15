from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
# Assuming these are defined in your project
from .serializers import UserProfileSerializer
from .models import UserProfile
import pdfplumber

class UserProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            # Update email field on retrieval (optional, but keeps data fresh)
            profile.email = request.user.email
            profile.save()
        except UserProfile.DoesNotExist:
            # You might want to automatically create a profile here if it's missing
            return Response({"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND)
            
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
            text = ""

            # --- FIX: Check if the file exists before accessing .path ---
            if profile.cv_pdf:
                try:
                    pdf_path = profile.cv_pdf.path
                    print(pdf_path)

                    with pdfplumber.open(pdf_path) as pdf:
                        for page in pdf.pages:
                            page_text = page.extract_text()
                            if page_text:
                                text += page_text + "\n"
                            else:
                                text += "[NO TEXT FOUND ON PAGE]\n"
                    
                    # Update the extracted text fields after successful extraction
                    new_text = text.lower()
                    profile.pdf_text = new_text

                except Exception as e:
                    # Catch errors related to pdfplumber or file reading (e.g., file not found, bad PDF)
                    print(f"Error processing PDF file: {e}")
                    # You may choose to skip the text update and return a warning, 
                    # or stop the whole PUT request with an error.
                    return Response({"error": f"Error processing CV PDF file: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                # If no file is associated, ensure pdf_text is reset or handled
                profile.pdf_text = ""
                print("No CV PDF file associated with this profile. Skipping PDF text extraction.")
            # --- END FIX ---
            
            # These are model updates applied regardless of file extraction success
            profile.email = request.user.email
            profile.save() # Save the email and pdf_text update 

        except UserProfile.DoesNotExist:
            return Response({"detail": "Profile not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Now, update the profile with incoming request data (e.g., name, phone)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)