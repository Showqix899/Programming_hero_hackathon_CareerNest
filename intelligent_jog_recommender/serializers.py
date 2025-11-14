from rest_framework import serializers


class TimeframeSerializer(serializers.Serializer):

    time_frame = serializers.CharField(required=True)
    