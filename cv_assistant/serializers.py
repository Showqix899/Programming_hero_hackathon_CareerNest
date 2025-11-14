from rest_framework import serializers


class CVAssistantSerializer(serializers.Serializer):
    cv_output = serializers.CharField()
