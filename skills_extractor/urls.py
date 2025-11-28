from django.urls import path
from .views import SkillExtractionView,UserSkillsView

urlpatterns = [
    path('extract-skills/', SkillExtractionView.as_view(), name='extract-skills'),
    path('user-skills/', UserSkillsView.as_view(), name='user-skills'),
]
