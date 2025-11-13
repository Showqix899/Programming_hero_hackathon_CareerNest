from rest_framework.routers import DefaultRouter
from .views import LearningResourceViewSet, AdminLearingResourceViewSet

router = DefaultRouter()
router.register(r'learning-resources', LearningResourceViewSet, basename='learning-resource')
router.register(r'admin/learning-resources', AdminLearingResourceViewSet, basename='admin-learning-resource')
urlpatterns = router.urls
