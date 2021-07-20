"""Lands model."""

# Django
from django.db import models

# Utilities
from farm_management.utils.models import FarmModel


class Land(FarmModel):
    """Land model

    A land is a certain amount of land on which agricultural
    or animal activities can occur.
    """

    name = models.CharField('land name', max_length=150)
    manager = models.ForeignKey('users.User', on_delete=models.CASCADE)
    location = models.CharField('land location', max_length=150)

    def __str__(self):
        """Return land name."""
        return self.name
