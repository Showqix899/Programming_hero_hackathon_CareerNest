from django.urls import path
from .views import CVAssistantView

urlpatterns = [
    path("ai/cv-assistant/", CVAssistantView.as_view(), name="cv-assistant"),
]
