from django.urls import path
from .views import SkillExtractionView

urlpatterns = [
    path('extract-skills/', SkillExtractionView.as_view(), name='extract-skills'),
]
