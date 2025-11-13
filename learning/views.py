from rest_framework import viewsets, permissions
from .models import LearningResource
from .serializers import LearningResourceSerializer

class LearningResourceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LearningResource.objects.all()
    serializer_class = LearningResourceSerializer
    permission_classes = [permissions.AllowAny]


class AdminLearingResourceViewSet(viewsets.ModelViewSet):
    queryset = LearningResource.objects.all()
    serializer_class = LearningResourceSerializer
    permission_classes = [permissions.IsAdminUser]
    
