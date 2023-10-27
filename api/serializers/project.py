from rest_framework import serializers

from api.models.project import Project, Issue, Comment


class ProjectCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create a Project
        - name, description and project_type are mandatory
    """

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "description",
            "project_type",
        ]

    # def validate_name(self, value):
    #     # check if name of the project already exists
    #     if Project.objects.filter(name=value).exists():
    #         raise serializers.ValidationError(
    #             "Attention! This project name exists already."
    #         )
    #     return value

    def validate(self, attrs):
        if Project.objects.filter(
            name=attrs["name"], project_type=attrs["project_type"]
        ).exists():
            raise serializers.ValidationError("Attention! This project exists already.")
        return attrs


class ProjectListSerializer(serializers.ModelSerializer):
    """
    display/lists selected information about the Project
    """

    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "author",
            "contributors",
        ]


class ProjectDetailSerializer(serializers.ModelSerializer):
    """
    display all information/details about the Project
    """

    class Meta:
        model = Project
        fields = [
            "id",
            "created_time",
            "name",
            "description",
            "project_type",
            "author",
            "contributors",
        ]

    """
    if the project gets bigger then it can be difficult
    to implement additional logic or causes errors
    class ProjectDetailSerializer(ProjectListSerializer):

        class Meta(ProjectListSerializer.Meta):
            model = Project
            fields = ProjectListSerializer.Meta.fields + [
                "created_time",
                "description",
                "project_type",
            ]
    """


class IssueCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create an Issue
        - mandatory fields: name, description, state, tag, priority and assigned_to
    """

    class Meta:
        model = Issue
        fields = [
            "id",
            "assigned_to",
            "name",
            "description",
            "tag",
            "state",
            "priority",
        ]

    def validate(self, attrs):
        if Issue.objects.filter(
            name=attrs["name"],
            tag=attrs["tag"],
            state=attrs["state"],
            priority=attrs["priority"],
        ).exists():
            raise serializers.ValidationError("This issue exists already!")

        return attrs


class IssueListSerializer(serializers.ModelSerializer):
    """
    displays/lists selected fields of the Issue model
    """

    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
            "assigned_to",
            "name",
            "description",
            "tag",
            "state",
            "priority",
            "project",
        ]


class IssueDetailSerializer(serializers.ModelSerializer):
    """
    displays all fields of the Issue model
    """

    class Meta:
        model = Issue
        fields = [
            "id",
            "created_time",
            "author",
            "assigned_to",
            "name",
            "description",
            "tag",
            "state",
            "priority",
            "project",
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    """
    serializer to create a Comment
        - mandatory fields: name and description
    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "name",
            "description",
        ]

    def validate_name(self, value):
        if Comment.objects.filter(name=value).exists():
            raise serializers.ValidationError("This comment name exists already.")

        return value


class CommentListSerializer(serializers.ModelSerializer):
    """
    displays selected fields of the Comment model
    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "author",
            "name",
            "issue",
        ]


class CommentDetailSerializer(serializers.ModelSerializer):
    """
    displays the fields of the Comment model
    """

    class Meta:
        model = Comment
        fields = [
            "id",
            "uuid",
            "created_time",
            "author",
            "name",
            "description",
            "issue",
            "issue_url",
        ]
