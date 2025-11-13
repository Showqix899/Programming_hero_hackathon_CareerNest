from rest_framework import serializers
from jobs.models import Job
from learning.models import LearningResource


class JobRecommendationSerializer(serializers.ModelSerializer):
    matched_skills = serializers.ListField(child=serializers.CharField(), read_only=True)
    match_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'company', 'location',
            'required_skills', 'experience_level', 'job_type',
            'matched_skills', 'match_score'
        ]


class ResourceRecommendationSerializer(serializers.ModelSerializer):
    matched_skills = serializers.ListField(child=serializers.CharField(), read_only=True)
    match_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = LearningResource
        fields = [
            'id', 'title', 'platform', 'url', 'related_skills', 'cost',
            'matched_skills', 'match_score'
        ]
