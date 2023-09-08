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

        contributor = Contributor(
            user=user,
            project=project,
            type="P",
            role="A",
        )
        contributor.save()


class ContributorViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing contributors
    - The queryset is based on the project
    - A Contributor with role=author can create new Contributors with
        role=contributor and type=project
    - Display all Contributors related to the project mentioned in the url"""

    serializer_class = ContributorSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])
        project_user = Contributor.objects.filter(
            user=serializer.initial_data["user"]
        ).exists()

        if not project_user:
            serializer.save(project=project, type="P", role="CO")

    def get_queryset(self):
        return Contributor.objects.filter(project_id=self.kwargs["project_pk"])


class IssueViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing issues
    - The queryset is based on the project
    - A Contributor with role=author can create new Contributors with
        role=contributor and type=issue
        and assign this contributor."""

    serializer_class = IssueSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user.username)
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        # check if the contributor with role="CO" already exists:
        assigned_to_exists = Contributor.objects.filter(
            user_id=serializer.validated_data["assigned_to"].id,
            type="I",
            role="CO",
        ).exists()

        if not assigned_to_exists:
            author = Contributor(
                user=user,
                project=project,
                type="I",
                role="A",
            )
            author.save()

            contributor = Contributor(
                user_id=serializer.validated_data["assigned_to"].id,
                project=project,
                type="I",
                role="CO",
            )
            contributor.save()

            serializer.save(project=project, author=author, assigned_to=contributor)

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs["project_pk"])


class CommentViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing comments
    - A Contributor with role=author can create new Contributors with
        role=contributor and type=comment"""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        user = get_object_or_404(User, username=self.request.user.username)
        project = get_object_or_404(Project, id=self.kwargs.get("project_pk"))
        issue = get_object_or_404(Issue, id=self.kwargs.get("issue_pk"))
        project_user = project.project_contributors.filter(
            user=self.request.user
        ).exists()

        if project_user:
            contributor = Contributor(
                user=user,
                project=project,
                type="C",
                role="CO",
            )
            contributor.save()

            serializer.save(author=contributor, issue=issue)
