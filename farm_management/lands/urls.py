"""Lands URLs."""

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import lands as land_views
from .views import paddocks as paddock_views

router = DefaultRouter()
router.register("lands", land_views.LandViewSet, basename="land")
router.register(
    r'lands/(?P<id>[0-9]+)/paddocks',
    paddock_views.PaddockViewSet,
    basename='paddocks'
)

urlpatterns = router.urls
