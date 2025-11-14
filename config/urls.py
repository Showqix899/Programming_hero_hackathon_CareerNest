
from django.contrib import admin
from django.urls import path,include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

schema_view = get_schema_view(
    openapi.Info(
        title="Your Project API",
        default_version='v1',
        description="API documentation for your Django REST project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your@email.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [

    #-----------------------app urls-----------------------
    path("api/accounts/", include("accounts.urls")),
    path('api/profiles/', include('profiles.urls')),
    path('api/', include('jobs.urls')), # Including jobs app URLs
    path('api/', include('learning.urls')), # Including learning app URLs
    path('api/', include('recommendations.urls')), # Including recommendations app URLs
    path('api/', include('search.urls')), # Including search app URLs
    path('api/', include('skills_extractor.urls')),
    path('api/',include('intelligent_jog_recommender.urls')),



    #----------------swagger urls-----------------
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)