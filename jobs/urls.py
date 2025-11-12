from rest_framework.routers import DefaultRouter
from .views import JobViewSet, JobAdminViewSet

router = DefaultRouter()
router.register(r'jobs', JobViewSet, basename='job')
router.register(r'admin/jobs', JobAdminViewSet, basename='admin-job')

urlpatterns = router.urls
