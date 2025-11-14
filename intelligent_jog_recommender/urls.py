from django.urls import path
from .views import RecommendationsView,RecommendationsWithSkillGapView,RoadmapGenerator

urlpatterns = [
    path('ai/recommendation/', RecommendationsView.as_view(), name='ai-recommendations'),
    path('ai/skill-learning/recommendation/',RecommendationsWithSkillGapView.as_view(),name="ai-skill-gap-resources"),
    path('ai/roadmap/generator/',RoadmapGenerator.as_view(),name="roadmap-generator")
]
