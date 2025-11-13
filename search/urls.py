from django.urls import path
from .views import SearchView, FilterView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('filter/', FilterView.as_view(), name='filter'),
]
