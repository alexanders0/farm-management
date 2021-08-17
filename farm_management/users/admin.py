from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from farm_management.users.forms import UserChangeForm, UserCreationForm

# Models
from farm_management.users.models import Profile
User = get_user_model()


class ProfileInline(admin.StackedInline):
    """ Profile in-line admin por users """

    model = Profile
    can_delete = False
    verbose_name_plural = 'profiles'


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    inlines = (ProfileInline,)
    list_display = ["username", "name", "is_superuser", "is_verified"]
    search_fields = ["name"]


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile model admin."""

    list_display = ('user', 'picture', 'biography')
    search_fields = ('user__username', 'user__email', 'user__name')

    fieldsets = (
        ('Profile', {
            'fields': (
                ('user', 'picture'),
                ('biography')
            )
        }),
        ('Metadata', {
            'fields': (('created', 'modified'),),
        })
    )

    readonly_fields = ('created', 'modified')
