from rest_framework import serializers

from ..models.project import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    """Project Serializer
    display the human-readable value instead of the database value"""

    class Meta:
        model = Project
        fields = "__all__"


class ContributorSerializer(serializers.ModelSerializer):
    """Contributor Serializer
    display the human-readable value instead of the database value"""

    class Meta:
        model = Contributor
        fields = "__all__"


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        # use all fields but organize them different
        fields = [
            "name",
            "description",
            "state",
            "tag",
            "priority",
            "project",
        ]
        # read_only_fields = ("project", "")


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
