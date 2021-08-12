"""Land models admin."""

# Django
from django.contrib import admin

# Model
from farm_management.lands.models import (
    Land,
    Paddock
)


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    """Land admin."""

    list_display = ['name', 'manager', 'location']
    search_fields = ['name', 'location']


@admin.register(Paddock)
class PaddockAdmin(admin.ModelAdmin):
    """Paddock admin."""

    list_display = ['name', 'description', 'meassure', 'is_active', 'land']
    search_fields = ['name', 'description']
