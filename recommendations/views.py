from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from profiles.models import UserProfile
from jobs.models import Job
from learning.models import LearningResource
from .serializers import JobRecommendationSerializer, ResourceRecommendationSerializer


class RecommendationsView(APIView):
    """
    Matches user's skills and career interests with Jobs and Learning Resources.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            return Response({'detail': 'User profile not found.'}, status=status.HTTP_404_NOT_FOUND)

        # --- Extract user skills and career interests ---
        user_skills = [s.strip().lower() for s in (profile.skills or "").split(',') if s.strip()]
        user_interests = [i.strip().lower() for i in (profile.career_interests or "").split(',') if i.strip()]

        # --- Match Jobs ---
        matched_jobs = []
        for job in Job.objects.all():
            job_skills = [s.lower() for s in job.required_skills]
            overlap = list(set(user_skills) & set(job_skills))
            score = len(overlap)
            if score > 0:
                job_data = JobRecommendationSerializer(job).data
                job_data["matched_skills"] = overlap
                job_data["match_score"] = score
                matched_jobs.append(job_data)

        # --- Match Learning Resources ---
        matched_resources = []
        for res in LearningResource.objects.all():
            res_skills = [s.lower() for s in res.related_skills]
            overlap = list(set(user_skills + user_interests) & set(res_skills))
            score = len(overlap)
            if score > 0:
                res_data = ResourceRecommendationSerializer(res).data
                res_data["matched_skills"] = overlap
                res_data["match_score"] = score
                matched_resources.append(res_data)

        return Response({
            "user": profile.email or str(profile.user),
            "skills": user_skills,
            "career_interests": user_interests,
            "recommended_jobs": sorted(matched_jobs, key=lambda x: x["match_score"], reverse=True),
            "recommended_resources": sorted(matched_resources, key=lambda x: x["match_score"], reverse=True)
        }, status=status.HTTP_200_OK)
