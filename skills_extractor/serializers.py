from rest_framework import serializers

class ExtractedDataSerializer(serializers.Serializer):
    skills = serializers.ListField(child=serializers.CharField())
    tools = serializers.ListField(child=serializers.CharField())
    roles = serializers.ListField(child=serializers.CharField())

