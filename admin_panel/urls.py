from django.urls import path
from rest_framework.routers import DefaultRouter
from jobs.views import JobAdminViewSet
from .views import UserAdminViewSets
from learning.views import AdminLearingResourceViewSet
router = DefaultRouter()
router.register(r'admin/jobs/', JobAdminViewSet, basename='admin-job')
router.register(r'admin/users/',UserAdminViewSets,basename='admin-user')
router.register(r'admin/learing-resource-controll/',AdminLearingResourceViewSet,basename='learning-resource-controll')

urlpatterns = router.urls



