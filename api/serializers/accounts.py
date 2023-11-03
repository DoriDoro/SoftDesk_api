from rest_framework import serializers
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
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


class UserDetailSerializer(serializers.ModelSerializer):
    """
    User Serializer, get all details of a User
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
            "date_joined",
        ]


class ContributorSerializer(serializers.ModelSerializer):
    """
    User/Contributor Serializer
    - selected information about the User
    """

    # create attribute 'user', which is write_only because we just need to give a value
    user = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserModel
        fields = ["id", "user"]

    def validate_user(self, value):
        user = UserModel.objects.filter(pk=value).first()

        if user is None:
            raise serializers.ValidationError("User does not exists!")

        if user.is_superuser:
            raise serializers.ValidationError(
                "Superusers cannot be added as contributors."
            )

        if self.context["view"].project.contributors.filter(pk=value).exists():
            raise serializers.ValidationError(
                "This user is already a contributor of this project."
            )

        return user


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
