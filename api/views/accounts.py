from rest_framework import viewsets

from ..models.accounts import User
from ..serializers.accounts import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """A simple ViewSet for viewing and editing users"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
