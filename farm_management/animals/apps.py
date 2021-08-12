"""Animals app."""

# Django
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AnimalsConfig(AppConfig):
    """Animals app config."""

    name = "farm_management.animals"
    verbose_name = _("Animals")
