from rest_framework import serializers

from ..models.project import Project, Issue, Comment

# short: from ..models import Project, Contributor, Issue, Comment

# TODO: instead of '__all__' (bad practise) choose the fields


class ProjectSerializer(serializers.ModelSerializer):
    """Project Serializer
    display the human-readable value instead of the database value"""

    class Meta:
        model = Project
        fields = ["id", "name", "description", "project_type", "author", "contributors"]


class IssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issue
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
