from rest_framework import serializers

from ..models.accounts import User


class UserSerializer(serializers.ModelSerializer):
    """User Serializer"""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]

    # hashes password before displaying raw password on api
    # TODO: use djangorestframework-simplejwt to hash the password (validate_password())
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
