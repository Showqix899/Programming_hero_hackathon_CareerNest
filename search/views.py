from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,permissions
from django.db.models import Q
from jobs.models import Job
from learning.models import LearningResource
from jobs.serializers import JobSerializer
from learning.serializers import LearningResourceSerializer


#search view
class SearchView(APIView):
    permission_classes=[permissions.AllowAny]
    def get(self, request):
        query = request.query_params.get('q', '').strip().lower()

        if not query:
            return Response({"detail": "Please provide a search query (?q=...)"},
                            status=status.HTTP_400_BAD_REQUEST)

        # Search in Jobs
        jobs = Job.objects.filter(
            Q(title__icontains=query) |
            Q(company__icontains=query) |
            Q(location__icontains=query) |
            Q(required_skills__icontains=query)
        )

        # Search in Learning Resources
        resources = LearningResource.objects.filter(
            Q(title__icontains=query) |
            Q(platform__icontains=query) |
            Q(related_skills__icontains=query)
        )

        return Response({
            "query": query,
            "results": {
                "jobs": JobSerializer(jobs, many=True).data,
                "learning_resources": LearningResourceSerializer(resources, many=True).data
            }
        }, status=status.HTTP_200_OK)


class JobFilterView(APIView):
   
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skill = request.query_params.get('skill', '').lower()
        job_type = request.query_params.get('job_type')
        location = request.query_params.get('location')

        queryset = Job.objects.all()

        if skill:
            queryset = queryset.filter(required_skills__icontains=skill)
        if job_type:
            queryset = queryset.filter(job_type__iexact=job_type)
        if location:
            queryset = queryset.filter(location__iexact=location)

        serializer = JobSerializer(queryset, many=True)
        return Response({
            "filters": {"skill": skill, "job_type": job_type, "location": location},
            "results": serializer.data
        }, status=status.HTTP_200_OK)



class ResourceFilterView(APIView):
    
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        skill = request.query_params.get('skill', '').lower()
        cost = request.query_params.get('cost')

        queryset = LearningResource.objects.all()

        if skill:
            queryset = queryset.filter(related_skills__icontains=skill)
        if cost:
            queryset = queryset.filter(cost__iexact=cost)

        serializer = LearningResourceSerializer(queryset, many=True)
        return Response({
            "filters": {"skill": skill, "cost": cost},
            "results": serializer.data
        }, status=status.HTTP_200_OK)