from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from ..models.accounts import User

from ..serializers.accounts import UserSerializer


class UserViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing user instances."""

    serializer_class = UserSerializer
    queryset = User.objects.all()


class RegisterView(generics.CreateAPIView):
    """Register a view"""

    serializer_class = UserSerializer
