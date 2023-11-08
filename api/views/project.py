from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

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
from api.views.mixins import SerializerClassMixin

UserModel = get_user_model()


class ProjectViewSet(SerializerClassMixin, ModelViewSet):
    serializer_class = ProjectCreateSerializer
    serializer_create_class = ProjectCreateSerializer
    serializer_detail_class = ProjectDetailSerializer
    serializer_list_class = ProjectListSerializer
    permission_classes = [IsAuthor, IsAuthenticated]

    _project = None

    @property
    def project(self):
        if self._project is None:
            self._project = Project.objects.filter(contributors=self.request.user)

        return self._project

    def get_queryset(self):
        # use order_by to avoid the warning for the pagination
        return self.project.order_by("created_time")

    def perform_create(self, serializer):
        # save the author as author and as contributor (request.user)
        serializer.save(author=self.request.user, contributors=[self.request.user])


class ContributorViewSet(ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing contributors/users
    - The queryset is based on the contributors of a project
    - Display all contributors/Users related to the project mentioned in the url
    """

    serializer_class = ContributorSerializer
    permission_classes = [IsProjectAuthorOrContributor]

    _project = None  # create this variable to avoid unnecessary database queries

    @property
    def project(self):
        """create an attribute project inside the ContributorViewSet
        this attribute is available in the view and can be called/available in the serializer
        """

        # if the view was never executed before, will make the database query
        #   otherwise _project will have a value and no database query will be performed
        if self._project is None:
            self._project = get_object_or_404(
                Project.objects.all().prefetch_related("contributors"),
                pk=self.kwargs["project_pk"],
            )
        return self._project

    def get_queryset(self):
        # use the UserModel attribute 'date_joined' to order to avoid the pagination warning
        return self.project.contributors.all().order_by("date_joined")

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ContributorDetailSerializer

        return super().get_serializer_class()

    def perform_create(self, serializer):
        self.project.contributors.add(serializer.validated_data["user"])

    def perform_destroy(self, instance):
        self.project.contributors.remove(instance)


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
    serializer_list_class = IssueListSerializer
    permission_classes = [IsProjectAuthorOrContributor, IsAuthenticated]

    _issue = None

    @property
    def issue(self):
        if self._issue is None:
            self._issue = Issue.objects.filter(project_id=self.kwargs["project_pk"])

        return self._issue

    def get_queryset(self):
        return self.issue.order_by("created_time")

    def perform_create(self, serializer):
        contributor = serializer.validated_data["assigned_to"]
        project = get_object_or_404(Project, id=self.kwargs["project_pk"])

        serializer.save(
            author=self.request.user,
            assigned_to=contributor,
            project=project,
        )


class CommentViewSet(SerializerClassMixin, ModelViewSet):
    """
    A simple ViewSet for creating, viewing and editing comments
    - The queryset is based on the issue
    - Creates the issue_url
    """

    serializer_class = CommentCreateSerializer
    serializer_create_class = CommentCreateSerializer
    serializer_detail_class = CommentDetailSerializer
    serializer_list_class = CommentListSerializer
    permission_classes = [IsProjectAuthorOrContributor, IsAuthenticated]

    _comment = None

    @property
    def comment(self):
        if self._comment is None:
            self._comment = Comment.objects.filter(issue_id=self.kwargs["issue_pk"])

        return self._comment

    def get_queryset(self):
        return self.comment.order_by("created_time")

    def perform_create(self, serializer):
        project_pk = self.kwargs["project_pk"]
        issue_pk = self.kwargs["issue_pk"]
        issue = get_object_or_404(Issue, id=issue_pk)
        issue_url = f"{settings.BASE_URL}/api/projects/{project_pk}/issues/{issue_pk}/"

        serializer.save(author=self.request.user, issue=issue, issue_url=issue_url)
