from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models.accounts import User
from ..serializers.accounts import UserSerializer


class UserAPIView(APIView):
    """Allow just authenticated users to get access to url"""

    permission_classes = [AllowAny]

    def get(self, request, format=None):
        content = {"status": "request was permitted"}

        return Response(content)

    # queryset = User.objects.all()
    # serializer_class = UserSerializer
