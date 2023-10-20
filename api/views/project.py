from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model

from ..models.project import Project, Issue, Comment
from ..permissions import IsAuthor, IsProjectAuthorOrContributor
from ..serializers.accounts import ContributorSerializer
from ..serializers.project import (
    ProjectSerializer,
    IssueSerializer,
    CommentSerializer,
)

UserModel = get_user_model()


class ProjectViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing projects"""

    serializer_class = ProjectSerializer
    permission_classes = [IsAuthor]

    def get_queryset(self):
        return Project.objects.filter(contributors=self.request.user)

    def perform_create(self, serializer):
        # name and project_type already exists
        project_exists = Project.objects.filter(
            name=serializer.validated_data["name"],
            project_type=serializer.validated_data["project_type"],
        ).exists()

        if not project_exists:
            user = get_object_or_404(UserModel, username=self.request.user.username)

            if user:
                # save the author as author and as contributor (request.user)
                serializer.save(author=user, contributors=[user])


class ContributorViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing contributors/users
    - The queryset is based on the project
    - Display all contributors/Users related to the project mentioned in the url"""

    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthorOrContributor]

    # TODO: Green Code, for list and detail etc use different serializer_class

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs.get("project_pk"))
        return project.contributors.all()

    def perform_create(self, serializer):
        """to create an object"""

        project_id = self.kwargs.get("project_pk")
        contributor_id = serializer.initial_data["user"]

        # get the project and all contributors, just one database query
        project = (
            Project.objects.filter(pk=project_id)
            .prefetch_related("contributors")
            .first()
        )
        contributor = get_object_or_404(UserModel, pk=contributor_id)

        if contributor.is_superuser:
            data = {
                "code": "CONTRIBUTOR_IS_SUPERUSER",
                "detail": "This contributor can not be added.",
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)

        if project.contributors.filter(pk=contributor_id).exists():
            data = {
                "code": "CONTRIBUTOR_ALREADY_EXISTS",
                "detail": "This contributor is already part of the project.",
            }
            return Response(data, status.HTTP_400_BAD_REQUEST)

        project.contributors.add(contributor)

        data = {
            "code": "ADDED_CONTRIBUTOR_SUCCESSFULLY",
            "detail": "Added the contributor successfully.",
        }

        return Response(data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        """to delete an object, for DELETE"""

        # get the project to remove the contributor
        project_id = self.kwargs.get("project_pk")
        if project_id is not None:
            # to avoid unnecessary database query, to improve performance
            project = get_object_or_404(Project, pk=project_id)

            contributor_id = self.request.data.get("user")
            contributor = get_object_or_404(UserModel, pk=contributor_id)

            project.contributors.remove(contributor)

            return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing issues
    - The queryset is based on the project
    - A Contributor of the project can create a new Issue and assign it himself or to a Contributor
    """

    serializer_class = IssueSerializer
    permission_classes = [IsProjectAuthorOrContributor]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs.get("project_pk"))

    def perform_create(self, serializer):
        # check if issue already exists:
        issue_exists = Issue.objects.filter(
            name=serializer.validated_data["name"],
            tag=serializer.validated_data["tag"],
            state=serializer.validated_data["state"],
            priority=serializer.validated_data["priority"],
        ).first()

        if not issue_exists:
            user = get_object_or_404(UserModel, username=self.request.user.username)
            contributor = get_object_or_404(
                UserModel, pk=serializer.validated_data["assigned_to"].pk
            )
            project = get_object_or_404(Project, id=self.kwargs.get("project_pk"))

            serializer.save(author=user, assigned_to=contributor, project=project)


class CommentViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing comments"""

    serializer_class = CommentSerializer
    permission_classes = [IsProjectAuthorOrContributor]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs.get("issue_pk"))

    def perform_create(self, serializer):
        # check if comment exists:
        comment_exists = Comment.objects.filter(
            name=serializer.validated_data["name"]
        ).first()

        if not comment_exists:
            user = get_object_or_404(UserModel, username=self.request.user.username)
            project_pk = self.kwargs.get("project_pk")
            issue_pk = self.kwargs.get("issue_pk")
            issue = get_object_or_404(Issue, id=issue_pk)
            issue_url = (
                f"http://127.0.0.1:8000/api/projects/{project_pk}/issues/{issue_pk}/"
            )

            serializer.save(author=user, issue=issue, issue_url=issue_url)
