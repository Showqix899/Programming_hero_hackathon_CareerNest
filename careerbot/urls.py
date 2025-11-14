# careerbot/urls.py
from django.urls import path
from .views import CareerBotAPIView

urlpatterns = [
    path("careerbot/ask/", CareerBotAPIView.as_view(), name="careerbot-ask"),
]
