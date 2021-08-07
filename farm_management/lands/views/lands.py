"""Lands views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated
from farm_management.lands.permissions import IsLandOwner

# Serializers
from farm_management.lands.serializers import (
    LandModelSerializer,
    CreateLandSerializer
)

# Models
from farm_management.lands.models import Land


class LandViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin,
                  mixins.DestroyModelMixin,
                  viewsets.GenericViewSet):
    """Land view set"""

    def get_queryset(self):
        """Restrict list to lands created by the requesting user."""

        queryset = Land.objects.all()
        if self.action == 'list':
            return queryset.filter(manager=self.request.user)
        return queryset

    def get_serializer_class(self):
        """Return serializer based on action."""

        if self.action == 'create':
            return CreateLandSerializer
        return LandModelSerializer

    def get_permissions(self):
        """Assign permission based on action."""

        permissions = [IsAuthenticated]
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            permissions.append(IsLandOwner)
        return [p() for p in permissions]
