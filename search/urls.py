from django.urls import path
from .views import JobFilterView, ResourceFilterView, SearchView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path('filter/jobs/', JobFilterView.as_view(), name='filter-jobs'),
    path('filter/resources/', ResourceFilterView.as_view(), name='filter-resources'),
]
