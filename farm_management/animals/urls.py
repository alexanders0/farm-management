"""Animals URLs."""

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import animals as animal_views

router = DefaultRouter()
router.register(
    r'lands/(?P<id>[0-9]+)/animals',
    animal_views.AnimalViewSet,
    basename='animal'
)

urlpatterns = router.urls
