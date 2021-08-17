"""User views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

# Permissions
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from farm_management.users.permissions import IsAccountOwner

# Serializers
from farm_management.users.serializers.profiles import ProfileModelSerializer
from farm_management.lands.serializers import LandModelSerializer
from farm_management.users.serializers import (
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    UserLoginSerializer
)

# Models
from django.contrib.auth import get_user_model
from farm_management.lands.models import Land

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.

    Handle sign up, login and account verification.
    """
    serializer_class = UserModelSerializer
    queryset = User.objects.filter(is_active=True)
    lookup_field = "username"

    def get_permissions(self):
        """Assign permissions based on action."""

        if self.action in ['signup', 'login', 'verify']:
            permissions = [AllowAny]
        elif self.action in ['retrieve', 'update', 'partial_update', 'profile']:
            permissions = [IsAuthenticated, IsAccountOwner]
        else:
            permissions = [IsAuthenticated]
        return [permission() for permission in permissions]

    def get_serializer_class(self):
        """Return serializer based on action."""

        if self.action == 'signup':
            return UserSignUpSerializer
        if self.action == 'verify':
            return AccountVerificationSerializer
        if self.action == 'login':
            return UserLoginSerializer
        return UserModelSerializer

    @action(detail=False, methods=['post'])
    def signup(self, request):
        """User sign up."""

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = UserModelSerializer(user).data
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def verify(self, request):
        """Account verification."""

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {'message': 'Congratulation, now go and manage farms!'}
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """User login."""

        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, token = serializer.save()
        data = {
            'user': UserModelSerializer(user).data,
            'token': token
        }
        return Response(data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['put', 'patch'], parser_classes=(MultiPartParser, ))
    def profile(self, request, *args, **kwargs):
        """Update profile data."""

        user = self.get_object()
        profile = user.profile
        partial = request.method == 'PATCH'
        serializer = ProfileModelSerializer(
            profile,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = UserModelSerializer(user).data
        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        """Add extra data to the response."""

        response = super(UserViewSet, self).retrieve(request, *args, **kwargs)
        lands = Land.objects.filter(manager=request.user)
        data = {
            'user': response.data,
            'lands': LandModelSerializer(lands, many=True).data
        }
        response.data = data
        return response
