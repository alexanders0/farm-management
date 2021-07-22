from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from farm_management.users.api.views import UserViewSet
from farm_management.lands.views import LandViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register(r"lands", LandViewSet)


app_name = "api"
urlpatterns = router.urls
