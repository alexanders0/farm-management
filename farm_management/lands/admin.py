"""Land models admin."""

# Django
from django.contrib import admin

# Model
from farm_management.lands.models import Land


@admin.register(Land)
class LandAdmin(admin.ModelAdmin):
    """Land admin."""

    list_display = ['name', 'manager', 'location']
    search_fields = ['name', 'location']
