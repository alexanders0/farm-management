"""Group serializers."""

# Django REST Framework
from farm_management.lands.models.paddocks import Paddock
from rest_framework import serializers

# Model
from farm_management.animals.models import Group
from farm_management.lands.models import Paddock


class GroupModelSerializer(serializers.ModelSerializer):
    """Group model serializer."""

    class Meta:
        """Meta class."""

        model = Group
        fields = '__all__'

    def update(self, instance, data):
        """ Update group and is_active flag of Paddock """

        if instance.location is not None:
            instance.location.is_active = False
            instance.location.save()
        if data['location'] is not None:
            data['location'].is_active = True
            data['location'].save()
        return super(GroupModelSerializer, self).update(instance, data)


class CreateGroupSerializer(serializers.ModelSerializer):
    """Create group serializer."""

    class Meta:
        """Meta class."""

        model = Group
        exclude = ('land', 'created', 'modified')

    def create(self, data):
        """Create group."""

        land = self.context['land']
        group = Group.objects.create(**data, land=land)
        if data['location'] is not None:
            paddock = Paddock.objects.get(pk=data['location'].pk)
            paddock.is_active = True
            paddock.save()

        return group
