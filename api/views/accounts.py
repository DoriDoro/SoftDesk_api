from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from api.serializers.accounts import UserCreateSerializer, UserDetailSerializer
from api.views.mixins import SerializerClassMixin

UserModel = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    Register a User
    """

    serializer_class = UserCreateSerializer


class UserViewSet(SerializerClassMixin, ModelViewSet):
    """
    A ViewSet for viewing and deleting a User
    """

    serializer_class = UserCreateSerializer
    serializer_detail_class = UserDetailSerializer

    def get_queryset(self):
        return UserModel.objects.all().order_by("date_joined")
