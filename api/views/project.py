from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model

from api.models.project import Project, Issue, Comment
from api.permissions import IsAuthor, IsProjectAuthorOrContributor
from api.serializers.accounts import (
    ContributorListSerializer,
    ContributorDetailSerializer,
)
from api.serializers.project import (
    ProjectCreateSerializer,
    ProjectListSerializer,
    ProjectDetailSerializer,
    IssueCreateSerializer,
    IssueListSerializer,
    IssueDetailSerializer,
    CommentCreateSerializer,
    CommentListSerializer,
    CommentDetailSerializer,
)

UserModel = get_user_model()


class SerializerClassMixin:
    serializer_class = None
    serializer_create_class = None
    serializer_detail_class = None

    def get_serializer_class(self):
        if self.action == "create":
            return self.serializer_create_class
        elif self.action == "list":
            return self.serializer_class
        elif self.action == "retrieve":
            return self.serializer_detail_class
        return super().get_serializer_class()


class ProjectViewSet(SerializerClassMixin, ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing projects
    """

    serializer_class = ProjectListSerializer
    serializer_create_class = ProjectCreateSerializer
    serializer_detail_class = ProjectDetailSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(contributors=self.request.user)

    def perform_create(self, serializer):
        # save the author as author and as contributor (request.user)
        serializer.save(author=self.request.user, contributors=[self.request.user])

        return super().perform_create(serializer)


class ContributorViewSet(SerializerClassMixin, ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing contributors/users
    - The queryset is based on the contributors of a project
    - Display all contributors/Users related to the project mentioned in the url
    """

    serializer_class = ContributorListSerializer
    serializer_detail_class = ContributorDetailSerializer
    permission_classes = [IsProjectAuthorOrContributor]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs.get("project_pk"))
        return project.contributors.all()

    def perform_create(self, serializer):
        """to add new contributor to project"""

        project_id = self.kwargs.get("project_pk")
        contributor_id = serializer.initial_data["user"]

        # get the project and all contributors with just one database query
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
        """to delete an contributor, for DELETE"""

        # get the project to remove the contributor
        project_id = self.kwargs.get("project_pk")
        if project_id is not None:
            # to avoid unnecessary database query, to improve performance
            project = get_object_or_404(Project, pk=project_id)

            contributor_id = self.request.data.get("user")
            contributor = get_object_or_404(UserModel, pk=contributor_id)

            project.contributors.remove(contributor)

            return Response(status=status.HTTP_204_NO_CONTENT)


class IssueViewSet(SerializerClassMixin, ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing issues
    - The queryset is based on the project
    - A contributor of the project can create a new Issue and assign it to himself
        or to another contributor
    """

    serializer_class = IssueListSerializer
    serializer_create_class = IssueCreateSerializer
    serializer_detail_class = IssueDetailSerializer
    permission_classes = [IsProjectAuthorOrContributor, IsAuthenticated]

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs.get("project_pk"))

    def perform_create(self, serializer):
        contributor = get_object_or_404(
            UserModel, pk=serializer.validated_data["assigned_to"].pk
        )
        project = get_object_or_404(Project, id=self.kwargs.get("project_pk"))

        serializer.save(
            author=self.request.user, assigned_to=contributor, project=project
        )


class CommentViewSet(SerializerClassMixin, ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing comments
    - The queryset is based on the issue
    - Creates the issue_url
    """

    serializer_class = CommentListSerializer
    serializer_create_class = CommentCreateSerializer
    serializer_detail_class = CommentDetailSerializer
    permission_classes = [IsProjectAuthorOrContributor, IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs.get("issue_pk"))

    def perform_create(self, serializer):
        project_pk = self.kwargs.get("project_pk")
        issue_pk = self.kwargs.get("issue_pk")
        issue = get_object_or_404(Issue, id=issue_pk)
        issue_url = (
            f"http://127.0.0.1:8000/api/projects/{project_pk}/issues/{issue_pk}/"
        )

        serializer.save(author=self.request.user, issue=issue, issue_url=issue_url)
