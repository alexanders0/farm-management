"""Breeds views."""

# Django REST Framework
from rest_framework import mixins, viewsets

# Permissions
from rest_framework.permissions import IsAuthenticated

# Serializers
from farm_management.animals.serializers import BreedModelSerializer

# Models
from farm_management.animals.models import Breed


class BreedViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Breed view set."""

    serializer_class = BreedModelSerializer
    queryset = Breed.objects.all()

    def get_permissions(self):
        """Assign permission based on action."""

        permissions = [IsAuthenticated]
        return [p() for p in permissions]
