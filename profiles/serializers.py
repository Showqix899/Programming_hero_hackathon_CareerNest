from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email','skills', 'experience', 'career_interests', 'cv_text','cv_pdf','pdf_text']
        read_only_fields = ['email','pdf_text']