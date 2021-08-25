"""Breed serializers."""

# Django REST Framework
from rest_framework import serializers

# Model
from farm_management.animals.models import Breed


class BreedModelSerializer(serializers.ModelSerializer):
    """Breed model serializer."""

    class Meta:
        """Meta class."""

        model = Breed
        fields = '__all__'
