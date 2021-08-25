"""Groups views."""

# Django REST Framework
from rest_framework import mixins, viewsets
from rest_framework.generics import get_object_or_404

# Permissions
from rest_framework.permissions import IsAuthenticated
from farm_management.animals.permissions import IsLandOwner

# Serializers
from farm_management.animals.serializers import (
    GroupModelSerializer,
    CreateGroupSerializer
)

# Models
from farm_management.animals.models import Group
from farm_management.lands.models import Land
from farm_management.lands.models import Paddock


class GroupViewSet(mixins.CreateModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.ListModelMixin,
                   mixins.DestroyModelMixin,
                   viewsets.GenericViewSet):
    """Group view set."""

    serializer_class = GroupModelSerializer

    def dispatch(self, request, *args, **kwargs):
        """Verify that the land exists."""

        id = kwargs['id']
        self.land = get_object_or_404(Land, id=id)
        return super(GroupViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        """Assign permission based on action."""

        permissions = [IsAuthenticated, IsLandOwner]
        return [p() for p in permissions]

    def get_queryset(self):
        """Restrict the list of groups belonging to the land specified in URI."""

        if getattr(self, 'swagger_fake_view', False):
            queryset = Group.objects.filter(land=None)
        else:
            queryset = Group.objects.filter(land=self.land)
        return queryset

    def get_serializer_context(self):
        """Add land to serializer context."""

        context = super(GroupViewSet, self).get_serializer_context()
        if getattr(self, 'swagger_fake_view', False):
            context['land'] = None
        else:
            context['land'] = self.land
        return context

    def get_serializer_class(self):
        """Return serializer based on action."""

        if self.action == 'create':
            return CreateGroupSerializer
        return GroupModelSerializer

    def perform_destroy(self, instance):
        """Update is_active flag of Paddock."""

        paddock = Paddock.objects.get(pk=instance.location.pk)
        paddock.is_active = False
        paddock.save()

        instance.delete()
