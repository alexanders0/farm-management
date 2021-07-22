"""Lands views."""

# Django REST Framework
from rest_framework import mixins, viewsets

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
                  viewsets.GenericViewSet):
    """Land view set"""

    queryset = Land.objects.all()

    def get_serializer_class(self):
        """ Return serializer based on action """

        if self.action == 'create':
            return CreateLandSerializer
        return LandModelSerializer
