from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model

from ..models.project import Project, Issue, Comment
from ..permissions import IsAuthorPermission, IsProjectContributorPermission
from ..serializers.accounts import UserSerializer
from ..serializers.project import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
)

UserModel = get_user_model()


class ProjectViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing projects
    Contributor as role=author is created"""

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    # permission_classes = [IsAuthenticated, AuthorPermission]

    def perform_create(self, serializer):
        user = UserModel.objects.filter(username=self.request.user.username).first()

        # if len(serializer.initial_data) == 4:
        #     contributors = UserModel.objects.filter(
        #         id__in=serializer.initial_data["contributors"]
        #     )

        if user:
            # save the author (request.user)
            serializer.save(author=user)


# class ContributorViewSet(ModelViewSet):
#     """A simple ViewSet for viewing and editing contributors/users
#     - The queryset is based on the project
#     - Display all contributors/Users related to the project mentioned in the url"""
#
#     serializer_class = ContributorSerializer
#     # permission_classes = [AuthorPermission]
#
#     def perform_create(self, serializer):
#         project_contributors = Project.objects.filter(
#             contributors=serializer.initial_data["id"]
#         ).exists()
#
#         if not project_contributors:
#             serializer.save(contributors=serializer.initial_data["id"])
#
#     def get_queryset(self):
#         return Project.objects.filter(id=self.kwargs["project_pk"])


class IssueViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing issues
    - The queryset is based on the project
    - A Contributor of the project can create a new Issue and assign it himself or to a Contributor
        will create 2 Contributors, one role="A" and second role="CO"."""

    serializer_class = IssueSerializer
    # permission_classes = [AuthorPermission]

    def perform_create(self, serializer):
        user = get_object_or_404(UserModel, username=self.request.user.username)
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        # TODO: error  raise self.model.MultipleObjectsReturned(
        # api.models.accounts.Contributor.MultipleObjectsReturned: get() returned more than one Contributor -- it returned 3!
        # for else statement

        serializer.save(
            project=project,
            author=user,
            assigned_to=Contributor.objects.get(
                user_id=serializer.validated_data["assigned_to"].id
            ),
        )

        # TODO: if assigned_to Contributor does not exist
        # raise self.model.DoesNotExist(
        # api.models.accounts.Contributor.DoesNotExist: Contributor matching query does not exist.

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs["project_pk"])


class CommentViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing comments
    - A Contributor with role=author can create new Contributors with role=contributor
    """

    serializer_class = CommentSerializer
    # permission_classes = [AuthorPermission]

    def perform_create(self, serializer):
        user = get_object_or_404(UserModel, username=self.request.user.username)
        project_pk = self.kwargs.get("project_pk")
        issue_pk = self.kwargs.get("issue_pk")
        project = get_object_or_404(Project, id=project_pk)
        issue = get_object_or_404(Issue, id=issue_pk)
        issue_url = (
            f"http://127.0.0.1:8000/api/projects/{project_pk}/issues/{issue_pk}/"
        )

        # check if the contributor with role="CO" already exists:
        author_exists = Contributor.objects.filter(
            user=self.request.user,
            role="A",
        ).exists()

        if not author_exists:
            contributor = Contributor(
                user=user,
                project=project,
                role="A",
            )
            contributor.save()

            serializer.save(author=contributor, issue=issue, issue_url=issue_url)

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs["issue_pk"])
