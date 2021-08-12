"""Breeds models."""

# Django
from django.db import models

# Utilities
from farm_management.utils.models import FarmModel


class Breed(FarmModel):
    """Breed model."""

    name = models.CharField('breed name', max_length=100)
    description = models.CharField('breed description', max_length=200)
    purpose = models.CharField('breed purpose', max_length=30)

    def __str__(self):
        """Return breed name."""
        return self.name
