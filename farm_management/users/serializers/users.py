"""User serializers."""

# Django
from django.conf import settings
from django.contrib.auth import password_validation, authenticate
from django.core.validators import RegexValidator

# Django REST Framework
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from rest_framework.validators import UniqueValidator

# Models
from django.contrib.auth import get_user_model
from farm_management.users.models import Profile

# Tasks
from farm_management.users.tasks import send_confirmation_email

# Serializers
from farm_management.users.serializers.profiles import ProfileModelSerializer

# Utilities
import jwt

User = get_user_model()


class UserModelSerializer(serializers.ModelSerializer):
    """User model serializer."""

    profile = ProfileModelSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = User
        fields = (
            "username",
            "name",
            "email",
            "phone_number",
            "profile"
        )

        extra_kwargs = {
            "url": {"view_name": "api:user-detail", "lookup_field": "username"}
        }


class UserSignUpSerializer(serializers.Serializer):
    """ User sign up serializer

    Handle sign up data validation and user/profile creation.
    """

    username = serializers.CharField(
        min_length=4,
        max_length=20,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Name
    name = serializers.CharField(min_length=2, max_length=100)

    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    # Phone number
    phone_regex = RegexValidator(
        regex=r'\+?1?\d{9,15}$',
        message='Phone number must be entered in the format: +9999999999. Up to 15 digits allowed.'
    )
    phone_number = serializers.CharField(validators=[phone_regex], max_length=17)

    # Password
    password = serializers.CharField(min_length=8, max_length=64)
    password_confirmation = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Verify password match."""

        passwd = data['password']
        passwd_conf = data['password_confirmation']
        if passwd != passwd_conf:
            raise serializers.ValidationError("Passwords don't match")
        password_validation.validate_password(passwd)
        return data

    def create(self, data):
        """Handle user and profile creation."""

        data.pop('password_confirmation')
        user = User.objects.create_user(**data, is_verified=False)
        Profile.objects.create(user=user)

        request = self.context['request']
        current_site = request.get_host()
        protocol = 'https://' if request.is_secure() else 'http://'
        send_confirmation_email.delay(
            user_pk=user.pk,
            current_site=current_site,
            protocol=protocol
        )

        return user


class UserLoginSerializer(serializers.Serializer):
    """User login serializer.

    Handle the login request data.
    """

    username = serializers.CharField(min_length=4, max_length=20)
    password = serializers.CharField(min_length=8, max_length=64)

    def validate(self, data):
        """Check credentials."""

        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError('Invalid credentials')
        if not user.is_verified:
            raise serializers.ValidationError('Account is not active yet :(')
        self.context['user'] = user
        return data

    def create(self, data):
        """Generate or retrieve new token."""

        token, created = Token.objects.get_or_create(user=self.context['user'])
        return self.context['user'], token.key
