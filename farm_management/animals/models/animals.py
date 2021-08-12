"""Animals models."""

# Django
from django.db import models
from django.db.models.deletion import CASCADE, SET_NULL

# Utilities
from farm_management.utils.models import FarmModel


class Animal(FarmModel):
    """Animal model."""

    name = models.CharField('animal name', max_length=150)
    birth_date = models.DateField()
    picture = models.ImageField(
        'animal picture',
        upload_to='animals/pictures',
        null=True,
        blank=True,
    )
    gender = models.CharField('animal gender', max_length=30)
    breed = models.ForeignKey(
        'animals.Breed',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    weight = models.FloatField(null=True)
    group = models.ForeignKey(
        'animals.Group',
        on_delete=SET_NULL,
        null=True,
        blank=True
    )
    land = models.ForeignKey(
        'lands.Land',
        on_delete=CASCADE
    )

    def __str__(self):
        """Return animal name."""
        return self.name
