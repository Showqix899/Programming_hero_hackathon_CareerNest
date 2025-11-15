from django.shortcuts import render
from accounts.models import User
from jobs.models import Job
from learning.models import LearningResource
from .serializers import UserAdminViewSeirailzers

# Create your views here.
from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated,IsAdminUser

#user admin view
class UserAdminViewSets(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserAdminViewSeirailzers
    permission_classes=[IsAuthenticated,IsAdminUser]
    


