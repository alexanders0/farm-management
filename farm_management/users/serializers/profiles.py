"""Profile serializers."""

# Django REST Framework
from rest_framework import serializers

# Models
from farm_management.users.models import Profile


class ProfileModelSerializer(serializers.ModelSerializer):
    """Profile model serializer."""

    class Meta:
        """Meta class."""

        model = Profile
        fields = (
            'picture',
            'biography'
        )
