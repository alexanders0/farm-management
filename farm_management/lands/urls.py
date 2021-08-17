"""Lands URLs."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import lands as land_views

router = DefaultRouter()
router.register("lands", land_views.LandViewSet, basename="land")

urlpatterns = router.urls
