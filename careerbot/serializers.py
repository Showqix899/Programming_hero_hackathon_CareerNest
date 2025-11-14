# careerbot/serializers.py
from rest_framework import serializers

class CareerBotRequestSerializer(serializers.Serializer):
    question = serializers.CharField()


