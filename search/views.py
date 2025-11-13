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



#filter view
class FilterView(APIView):
    
    permission_classes=[permissions.AllowAny]

    def get(self, request):
        data_type = request.query_params.get('type')  # "job" or "resource"
        skill = request.query_params.get('skill', '').lower()
        job_type = request.query_params.get('job_type')
        location = request.query_params.get('location')
        cost = request.query_params.get('cost')

        if data_type == 'job':
            queryset = Job.objects.all()

            if skill:
                queryset = queryset.filter(required_skills__icontains=skill)
            if job_type:
                queryset = queryset.filter(job_type__iexact=job_type)
            if location:
                queryset = queryset.filter(location__iexact=location)

            return Response({
                "filtered_jobs": JobSerializer(queryset, many=True).data
            }, status=status.HTTP_200_OK)

        elif data_type == 'resource':
            queryset = LearningResource.objects.all()

            if skill:
                queryset = queryset.filter(related_skills__icontains=skill)
            if cost:
                queryset = queryset.filter(cost__iexact=cost)

            return Response({
                "filtered_resources": LearningResourceSerializer(queryset, many=True).data
            }, status=status.HTTP_200_OK)

        else:
            return Response({"detail": "Invalid or missing 'type' parameter (use ?type=job or ?type=resource)."},
                            status=status.HTTP_400_BAD_REQUEST)
