from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User Serializer, used to register a new User
    """

    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "password",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]
        # do not display the password on api
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = UserModel(
            username=validated_data["username"],
            age=validated_data["age"],
            can_be_contacted=validated_data["can_be_contacted"],
            can_data_be_shared=validated_data["can_data_be_shared"],
        )
        user.set_password(validated_data["password"])
        user.save()

        return user


class ContributorListSerializer(serializers.ModelSerializer):
    """
    User/Contributor Serializer
    - selected information about the User
    """

    class Meta:
        model = UserModel
        fields = ["id", "username"]


class ContributorDetailSerializer(serializers.ModelSerializer):
    """
    User/Contributor Serializer
    - all details about the User
    """

    class Meta:
        model = UserModel
        fields = [
            "id",
            "username",
            "age",
            "can_be_contacted",
            "can_data_be_shared",
        ]
