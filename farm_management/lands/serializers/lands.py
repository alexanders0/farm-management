"""Land serializers."""

# Django REST Framework
from rest_framework import serializers

# Serializers
from farm_management.users.api.serializers import UserModelSerializer

# Model
from farm_management.lands.models import Land


class LandModelSerializer(serializers.ModelSerializer):
    """Land model serializer."""

    manager = UserModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = Land
        fields = (
            'id',
            'name',
            'manager',
            'location'
        )


class CreateLandSerializer(serializers.ModelSerializer):
    """Create land serializer."""

    manager = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        """Meta class."""

        model = Land
        fields = (
            'name',
            'manager',
            'location'
        )
