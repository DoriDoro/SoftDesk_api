from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

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

    @action(detail=True, url_path="contributors")
    def get_contributors(self, request, pk=None):
        contributors = Contributor.objects.filter(project=pk).order_by("role")
        serializer = ContributorSerializer(contributors, many=True)

        return Response(serializer.data)

    @action(detail=True, url_path="issues")
    def get_issues(self, request, pk=None):
        issues = Issue.objects.filter(project=pk)
        serializer = IssueSerializer(issues, many=True)

        return Response(serializer.data)

    @action(detail=True, url_path="issue/comments")
    def get_comments_for_issues(self, request, pk=None):
        comments = Comment.objects.filter(issue__project=pk)
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)

    def perform_create(self, serializer):
        project = serializer.save()
        user = self.request.user

        Contributor.objects.create(
            user=user,
            project=project,
            types="P",
            role="A",
        )

    # def list(self, request, *args, **kwargs):
    # get_user = request.user
    # queryset = Project.objects.

    # queryset = Project.objects.all()
    # serializer_class = ProjectSerializer


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
