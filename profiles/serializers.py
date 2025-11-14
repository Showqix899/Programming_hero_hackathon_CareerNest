from rest_framework import serializers
from .models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['email','skills', 'experience', 'career_interests', 'cv_text','cv_pdf']
        read_only_fields = ['email']