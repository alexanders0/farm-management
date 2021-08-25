"""Animals URLs."""

# Django REST Framework
from rest_framework.routers import DefaultRouter

# Views
from .views import animals as animal_views
from .views import breeds as breed_views
from .views import groups as group_views

router = DefaultRouter()
router.register(
    r'lands/(?P<id>[0-9]+)/animals',
    animal_views.AnimalViewSet,
    basename='animal'
)
router.register(r'breeds', breed_views.BreedViewSet, basename='breed')
router.register(
    r'lands/(?P<id>[0-9]+)/groups',
    group_views.GroupViewSet,
    basename='group'
)

urlpatterns = router.urls
