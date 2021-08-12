"""Groups models."""

# Django
from django.db import models

# Utilities
from farm_management.utils.models import FarmModel


class Group(FarmModel):
    """Group model."""

    name = models.CharField('group name', max_length=100)
    description = models.CharField('group description', max_length=200)
    location = models.ForeignKey(
        'lands.Paddock',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        """Return group name."""
        return self.name
