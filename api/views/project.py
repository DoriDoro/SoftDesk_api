from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model

from ..models.project import Project, Issue, Comment
from ..permissions import IsAuthor, IsProjectAuthor, IsProjectContributor
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
    # permission_classes = [IsAuthor]

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
    permission_classes = [IsProjectAuthor]

    # TODO: give contributors permission to add other contributors
    # TODO: if contributor has no permission for a project, instead of displaying an empty list,
    #    display a message: "You have no permission."
    # TODO: write permission that superuser can not be a contributor
    #    OR overwrite the save function in Project model
    # TODO: check if contributor is already in the list, if yes, message: "This contributor..."
    # TODO: message if contributor is added instead of {}, message: "Added contributor succ..."
    # TODO: if contributor is adding a contributor, it is working, WRONG

    def get_queryset(self):
        project = get_object_or_404(Project, pk=self.kwargs.get("project_pk"))
        return project.contributors.all()

    def perform_create(self, serializer):
        # check permissions result
        permission_result = self.check_permissions(self.request)
        print("here-----", permission_result)
        project = get_object_or_404(Project, pk=self.kwargs.get("project_pk"))

        contributor = get_object_or_404(UserModel, pk=serializer.initial_data["user"])
        # project.contributors.add(contributor)


class IssueViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing issues
    - The queryset is based on the project
    - A Contributor of the project can create a new Issue and assign it himself or to a Contributor
        will create 2 Contributors, one role="A" and second role="CO"."""

    serializer_class = IssueSerializer
    permission_classes = [IsProjectAuthor]

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

    def get_queryset(self):
        return Issue.objects.filter(project_id=self.kwargs.get("project_pk"))


class CommentViewSet(ModelViewSet):
    """A simple ViewSet for viewing and editing comments
    - A Contributor with role=author can create new Contributors with role=contributor
    """

    serializer_class = CommentSerializer
    permission_classes = [IsProjectAuthor]

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

    def get_queryset(self):
        return Comment.objects.filter(issue_id=self.kwargs.get("issue_pk"))
