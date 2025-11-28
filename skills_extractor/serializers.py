from rest_framework import serializers
from .models import UserSkills

class ExtractedDataSerializer(serializers.Serializer):
    skills = serializers.ListField(child=serializers.CharField())
    tools = serializers.ListField(child=serializers.CharField())
    roles = serializers.ListField(child=serializers.CharField())

class UserSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserSkills
        fields = ['id', 'user', 'skills', 'tools', 'roles']