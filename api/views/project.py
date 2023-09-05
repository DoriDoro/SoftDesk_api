from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

from ..models.accounts import User, Contributor
from ..models.project import Project, Issue, Comment
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

    # perform_create is the function which is saving the serializer
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

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user.username)
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        contributor = Contributor(
            user=user,
            project=project,
            types="C",
            role="A",
        )
        contributor.save()

        serializer.save(project=project, contributor=contributor)


class CommentViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing comments"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user.username)
        issue = get_object_or_404(Issue, id=self.kwargs.get("issue_pk"))
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        contributor = Contributor(
            user=user,
            project=project,
            types="C",
            role="A",
        )
        contributor.save()

        serializer.save(issue=issue, contributor=contributor)
