"""Land permission classes."""

# Django REST Framework
from rest_framework.permissions import BasePermission


class IsLandOwner(BasePermission):
    """Verify requesting user is the land creator."""

    def has_object_permission(self, request, view, obj):
        """Verify requesting user is the land creator."""

        return request.user == obj.manager
