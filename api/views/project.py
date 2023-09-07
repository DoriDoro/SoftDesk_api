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

        # check if the author assigned himself the issue:
        author_assign = Contributor.objects.filter(
            user=serializer.initial_data["assigned_to"],
            type="I",
            role="A",
        )
        # check if the contributor already exists:
        contributor = Contributor.objects.filter(
            user=serializer.initial_data["assigned_to"],
            type="I",
            role="CO",
        )

        print("here---", author_assign, "---", contributor)

        # if the request.user assign the issue to himself:
        if not contributor:
            if not author_assign:
                print("well done")

        # if no contributor with role='CO' for project exists
        if not contributor and not author_assign:
            print("check")
            # contributor = Contributor(
            #     user=user,
            #     project=project,
            #     type="I",
            #     role="CO",
            # )
            # contributor.save()
            #
            # serializer.save(project=project, author=contributor)
        # TODO: if not author created the contributor: message in Postman: not saved
        # TODO: if author assign it to itself

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
