from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from ..models.accounts import User
from ..models.project import Project, Contributor, Issue, Comment
from ..serializers.project import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing projects
    Contributor as role=author is created"""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        project = serializer.save()
        user = get_object_or_404(User, username=self.request.user.username)

        contributor_data = {
            "user": user.id,
            "project": project.id,
            "types": "P",
            "role": "A",
        }

        contributor_serializer = ContributorSerializer(data=contributor_data)
        contributor_serializer.is_valid(raise_exception=True)
        contributor_serializer.save()


class ContributorViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing contributors"""

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class IssueViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing issues"""

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing comments"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]
