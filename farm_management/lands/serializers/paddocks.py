"""Paddock serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from farm_management.lands.models import Paddock


class PaddockModelSerializer(serializers.ModelSerializer):
    """Paddock model """

    class Meta:
        """Meta class."""

        model = Paddock
        exclude = ('created', 'modified')
        read_only_fields = ('is_active',)


class CreatePaddockSerializer(serializers.ModelSerializer):
    """Create paddock serializer."""

    class Meta:
        """Meta class."""

        model = Paddock
        exclude = ('land', 'created', 'modified')
        read_only_fields = ('is_active',)

    def create(self, data):
        """Create paddock."""

        land = self.context['land']
        paddock = Paddock.objects.create(**data, land=land)
        return paddock
