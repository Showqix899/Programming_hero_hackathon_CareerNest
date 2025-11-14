from django.urls import path
from .views import RecommendationsView,RecommendationsWithSkillGapView,RoadmapGenerator

urlpatterns = [
    path('ai/job/recommendation/', RecommendationsView.as_view(), name='ai-recommendations'),
    path('ai/gap-analysis-and-learning-suggestions/',RecommendationsWithSkillGapView.as_view(),name="ai-skill-gap-resources"),
    path('ai/roadmap/generator/',RoadmapGenerator.as_view(),name="roadmap-generator")
]
