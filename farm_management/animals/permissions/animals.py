"""Animal permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from farm_management.animals.models import Animal
from farm_management.lands.models import Land


class IsLandOwner(BasePermission):
    """Verify requesting user is the land creator."""

    def has_permission(self, request, view):
        """Verify requesting user is the land creator."""

        try:
            Land.objects.get(
                id=view.land.pk,
                manager=request.user
            )
        except Land.DoesNotExist:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """Verify requesting user is the land creator."""

        return request.user == view.land.manager
