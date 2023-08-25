from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from ..models.project import Project, Contributor, Issue, Comment
from ..serializers.project import (
    ProjectSerializer,
    ContributorSerializer,
    IssueSerializer,
    CommentSerializer,
)


class ProjectViewSet(viewsets.ModelViewSet):
    """A simple ViewSet for viewing and editing projects"""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]


class ContributorViewSet(viewsets.ModelViewSet):
    """A simple ViewSet for viewing and editing contributors"""

    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class IssueViewSet(viewsets.ModelViewSet):
    """A simple ViewSet for viewing and editing issues"""

    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CommentViewSet(viewsets.ModelViewSet):
    """A simple ViewSet for viewing and editing comments"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
