"""Animals views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from farm_management.animals.permissions import IsLandOwner

# Serializers
from farm_management.animals.serializers import (
    AnimalModelSerializer,
    CreateAnimalSerializer
)

# Models
from farm_management.animals.models import Animal
from farm_management.lands.models import Land


class AnimalViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    """Animal view set."""

    def dispatch(self, request, *args, **kwargs):
        """Verify that the land exists."""

        id = kwargs['id']
        self.land = get_object_or_404(Land, id=id)
        return super(AnimalViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permission based on action."""

        permissions = [IsAuthenticated, IsLandOwner]
        return [p() for p in permissions]

    def get_queryset(self):
        """Restrict the list of animals belonging to the land specified in URI."""

        queryset = Animal.objects.filter(land=self.land)
        return queryset

    def get_serializer_context(self):
        """Add land to serializer context."""

        context = super(AnimalViewSet, self).get_serializer_context()
        context['land'] = self.land
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""

        if self.action == 'create':
            return CreateAnimalSerializer
        return AnimalModelSerializer