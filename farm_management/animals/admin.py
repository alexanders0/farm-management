"""Animal models admin."""

# Django
from django.contrib import admin

# Model
from farm_management.animals.models import (
    Animal,
    Group,
    Breed
)


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    """Animal admin."""

    list_display = ['name', 'gender', 'picture', 'breed', 'weight', 'land', 'group']
    search_fields = ['name', 'gender', 'breed']


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Group admin."""

    list_display = ['name', 'description', 'location']
    search_fields = ['name', 'description']


@admin.register(Breed)
class GroupAdmin(admin.ModelAdmin):
    """Breed admin."""

    list_display = ['name', 'description', 'purpose']
    search_fields = ['name', 'description', 'purpose']
