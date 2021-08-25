"""Animal serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from farm_management.animals.models import Animal


class AnimalModelSerializer(serializers.ModelSerializer):
    """Animal model serializer."""

    class Meta:
        """Meta class."""

        model = Animal
        fields = '__all__'


class CreateAnimalSerializer(serializers.ModelSerializer):
    """Create animal serializer."""

    class Meta:
        """Meta class."""

        model = Animal
        exclude = ('land',)

    def create(self, data):
        """Create animal."""

        land = self.context['land']
        animal = Animal.objects.create(**data, land=land)
        return animal
