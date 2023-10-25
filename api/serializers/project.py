from rest_framework import serializers

from ..models.project import Project, Issue, Comment


class ProjectListSerializer(serializers.ModelSerializer):
    """
    display selected information about the Project
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
    display all information about the Project
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


class IssueListSerializer(serializers.ModelSerializer):
    """
    displays selected fields of the Issue model
    """

    class Meta:
        model = Issue
        fields = [
            "id",
            "author",
            "assigned_to",
            "name",
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
