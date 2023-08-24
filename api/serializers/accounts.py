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
        # do not display the password on api
        # extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            age=validated_data["age"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user
