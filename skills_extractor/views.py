from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from profiles.models import UserProfile
from .extractor import extract_all
from .models import UserSkills
from .serializers import UserSkillsSerializer


class SkillExtractionView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        profile = request.user.profile
        
        try:
            user_skills = UserSkills.objects.get(user=request.user)

            # Convert stored key-value pairs → list of keys
            extracted_data = {
                "skills_found": list(user_skills.skills.keys()),
                "tools_found": list(user_skills.tools.keys()),
                "roles_found": list(user_skills.roles.keys()),
                "confidence_score": (
                    sum(user_skills.skills.values()) +
                    sum(user_skills.tools.values()) +
                    sum(user_skills.roles.values())
                )
            }

        except UserSkills.DoesNotExist:
            text_to_extract = " ".join(profile.pdf_text)
            if not text_to_extract:
                return Response({"detail": "No CV text found."}, status=status.HTTP_400_BAD_REQUEST)

            extracted_raw = extract_all(text_to_extract)

            # Save original dicts
            UserSkills.objects.create(
                user=request.user,
                skills=extracted_raw.get("skills_found", {}),
                tools=extracted_raw.get("tools_found", {}),
                roles=extracted_raw.get("roles_found", {})
            )

            # Convert → list for API response
            extracted_data = {
                "skills_found": list(extracted_raw.get("skills_found", {}).keys()),
                "tools_found": list(extracted_raw.get("tools_found", {}).keys()),
                "roles_found": list(extracted_raw.get("roles_found", {}).keys()),
                "confidence_score": extracted_raw.get("confidence_score", 0)
            }

        return Response({
            "user": profile.user.email,
            "skills_found": extracted_data["skills_found"],
            "tools_found": extracted_data["tools_found"],
            "roles_found": extracted_data["roles_found"],
            "confidence_score": extracted_data["confidence_score"]
        }, status=status.HTTP_200_OK)


#userview
class UserSkillsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            user_skills = UserSkills.objects.get(user=request.user)
            serializer = UserSkillsSerializer(user_skills)
            return Response({
                "user_skills": serializer.data
            }, status=status.HTTP_200_OK)
        except UserSkills.DoesNotExist:
            return Response({"detail": "No skills data found for the user."}, status=status.HTTP_404_NOT_FOUND)
        
        
    def patch(self, request):
        try:
            user_sills = UserSkills.objects.get(user=request.user)
        except UserSkills.DoesNotExist:
            return Response({"detail": "No skills data found for the user."}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSkillsSerializer(user_sills, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"user_skills": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def delete(self, request):
        try:
            user_skills = UserSkills.objects.get(user=request.user)
            user_skills.delete()
            return Response({"detail": "User skills data deleted."}, status=status.HTTP_204_NO_CONTENT)
        except UserSkills.DoesNotExist:
            return Response({"detail": "No skills data found for the user."}, status=status.HTTP_404_NOT_FOUND)