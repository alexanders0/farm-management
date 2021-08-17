"""Animal serializers."""

# Django REST Framework
from django.db.models import fields
from rest_framework import serializers

# Serializers
from farm_management.lands.serializers import LandModelSerializer

# Model
from farm_management.animals.models import Animal


class AnimalModelSerializer(serializers.ModelSerializer):
    """Animal model serializer."""

    # land = LandModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = Animal
        exclude = ('created', 'modified')
        # read_only_fields = ('land',)


class CreateAnimalSerializer(serializers.ModelSerializer):
    """Create animal serializer."""

    class Meta:
        """Meta class."""

        model = Animal
        exclude = ('land', 'created', 'modified')

    def create(self, data):
        """Create animal."""

        land = self.context['land']
        animal = Animal.objects.create(**data, land=land)
        return animal
