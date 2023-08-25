from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from ..models.accounts import User
from ..serializers.accounts import MyTokenObtainPairSerializer


# from ..serializers.accounts import UserSerializer


class UserAPIView(APIView):
    """Allow just authenticated users to get access to url"""

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        content = {"status": "request was permitted"}

        return Response(content)


class MyObtainTokenPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


# class UserViewSet(viewsets.ModelViewSet):
#     """A simple ViewSet for viewing and editing users"""
#
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
