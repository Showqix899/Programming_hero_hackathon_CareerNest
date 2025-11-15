from rest_framework.routers import DefaultRouter
from .views import LearningResourceViewSet, AdminLearingResourceViewSet

router = DefaultRouter()
router.register(r'learning-resources', LearningResourceViewSet, basename='learning-resource')

urlpatterns = router.urls
