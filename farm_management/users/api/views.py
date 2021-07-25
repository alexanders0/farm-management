"""User views."""

# Django REST Framework
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

# Serializers
from .serializers import (
    UserModelSerializer,
    UserSignUpSerializer,
    AccountVerificationSerializer,
    UserLoginSerializer
)

# Models
from django.contrib.auth import get_user_model

User = get_user_model()


class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """User view set.

    Handle sign up, login and account verification.
    """
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    lookup_field = "username"

    def get_queryset(self, *args, **kwargs):
        return self.queryset.filter(id=self.request.user.id)

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
