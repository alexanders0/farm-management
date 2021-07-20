"""Lands app."""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class LandsConfig(AppConfig):
    """Lands app config."""

    name = "farm_management.lands"
    verbose_name = _("Lands")
