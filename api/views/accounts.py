from rest_framework import generics

from api.serializers.accounts import UserSerializer


class RegisterView(generics.CreateAPIView):
    """
    Register a User
    """

    serializer_class = UserSerializer
