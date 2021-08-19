"""Paddocks views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from farm_management.animals.permissions import IsLandOwner

# Serializers
from farm_management.lands.serializers import (
    PaddockModelSerializer,
    CreatePaddockSerializer
)

# Models
from farm_management.lands.models import (
    Land,
    Paddock
)


class PaddockViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    """Paddock view set."""

    serializer_class = PaddockModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the land exists."""

        id = kwargs['id']
        self.land = get_object_or_404(Land, id=id)
        return super(PaddockViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permission based on action."""

        permissions = [IsAuthenticated, IsLandOwner]
        return [p() for p in permissions]

    def get_queryset(self):
        """Restrict the list of paddocks belonging to the land specified in URI."""

        if getattr(self, 'swagger_fake_view', False):
            queryset = Paddock.objects.filter(land=None)
        else:
            queryset = Paddock.objects.filter(land=self.land)
        return queryset

    def get_serializer_context(self):
        """Add land to serializer context."""

        context = super(PaddockViewSet, self).get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            context['land'] = None
        else:
            context['land'] = self.land
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""

        if self.action == 'create':
            return CreatePaddockSerializer
        return PaddockModelSerializer
