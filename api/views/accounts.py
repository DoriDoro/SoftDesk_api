from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from api.serializers.accounts import (
    UserCreateSerializer,
    UserDetailSerializer,
    UserListSerializer,
)
from api.views.mixins import SerializerClassMixin

UserModel = get_user_model()


class RegisterView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer


class UserViewSet(SerializerClassMixin, ModelViewSet):
    serializer_class = UserListSerializer
    serializer_create_class = UserCreateSerializer
    serializer_detail_class = UserDetailSerializer
    serializer_list_class = UserListSerializer

    def get_queryset(self):
        return UserModel.objects.all().order_by("date_joined")
