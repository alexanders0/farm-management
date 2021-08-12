"""Paddocks model."""

# Django
from django.db import models

# Utilities
from farm_management.utils.models import FarmModel


class Paddock(FarmModel):
    """Paddock model."""

    name = models.CharField('paddock name', max_length=150)
    description = models.CharField('paddock description', max_length=150)
    meassure = models.FloatField(null=True)
    is_active = models.BooleanField(
        'active status',
        default=False,
        help_text='It is used to know if a group of animals is currently using the paddock.'
    )
    land = models.ForeignKey(
        'lands.Land',
        on_delete=models.CASCADE
    )

    def __str__(self):
        """Return paddock name."""
        return self.name
