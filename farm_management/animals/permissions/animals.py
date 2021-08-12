"""Animal permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission

# Models
from farm_management.animals.models import Animal


class IsLandOwner(BasePermission):
    """Verify requesting user is the land creator."""

    def has_permission(self, request, view):
        """Verify requesting user is the land creator."""

        animals = Animal.objects.filter(
            land__manager=request.user,
            land=view.land
        )

        if not animals:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        """Verify requesting user is the land creator."""

        return request.user == view.land.manager
