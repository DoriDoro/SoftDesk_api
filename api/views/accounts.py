from rest_framework import generics

from ..serializers.accounts import UserSerializer


class RegisterView(generics.CreateAPIView):
    """Register a view"""

    serializer_class = UserSerializer
