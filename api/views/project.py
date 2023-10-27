from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model

from api.models.project import Project, Issue, Comment
from api.permissions import IsAuthor, IsProjectAuthorOrContributor
from api.serializers.accounts import (
    ContributorSerializer,
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


class ContributorViewSet(ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing contributors/users
    - The queryset is based on the contributors of a project
    - Display all contributors/Users related to the project mentioned in the url
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthorOrContributor]

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs.get("project_pk"))

        return project.contributors.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ContributorDetailSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        """to add new contributor to project"""

        project_id = self.kwargs.get("project_pk")
        contributor_id = serializer.initial_data["user_id"]

        # get the project and all contributors with just one database query
        project = (
            Project.objects.filter(pk=project_id)
            .prefetch_related("contributors")
            .first()
        )
        contributor = get_object_or_404(UserModel, pk=contributor_id)

        if contributor.is_superuser:
            raise ValidationError("Superusers cannot be added as contributors.")

        if project.contributors.filter(pk=contributor_id).exists():
            raise ValidationError("This user is already a contributor of this project.")

        project.contributors.add(contributor)

    def perform_destroy(self, instance):
        """to remove a contributor from a project, for DELETE"""

        # get the project to remove the contributor
        project_id = self.kwargs.get("project_pk")
        if project_id is not None:
            # to avoid unnecessary database query, to improve performance
            project = get_object_or_404(Project, pk=project_id)

            contributor_id = self.request.data.get("user_id")
            contributor = get_object_or_404(UserModel, pk=contributor_id)

            project.contributors.remove(contributor)


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
