from rest_framework.permissions import BasePermission, SAFE_METHODS

from api.models import Project


class IsAuthor(BasePermission):
    """Object-level permission to only allow authors to edit and delete an object"""

    message = "You have to be the author to update or delete."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsProjectAuthorOrContributor(BasePermission):
    """Object-level permission to only allow authors to edit and delete an object"""

    message = "You have to be the author to update or delete."

    def has_permission(self, request, view):
        # GET and POST
        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)

        # check if the request.user is a contributor
        if request.user in project.contributors.all():
            return True

    def has_object_permission(self, request, view, obj):
        # GET, POST, PUT, PATCH, DELETE with pk
        if request.method in SAFE_METHODS:
            return True

        project_id = view.kwargs.get("project_pk")
        project = Project.objects.get(pk=project_id)
        return project.author == request.user


# class IsProjectContributor(BasePermission):
#     """Permission to add other contributors when request.user is contributor of project"""
#
#     message = "You are no contributor of this project."
#
#     def has_object_permission(self, request, view, obj):
#         if request.method in SAFE_METHODS:
#             return True
#
#         # TODO after migrations add 's' to project_contributor
#         project_contributor = obj.project_contributor
#         return request.user in project_contributor


# class IsProjectContributor(BasePermission):
#     """Permission to have a Read-Only-Permission"""
#
#     message = "You have a ready only permission."
#
#     def has_permission(self, request, view):
#         # TODO after migrations add 's' to project_contributor
#         return request.user.project_contributor.filter(pk=request.data["user"]).exists()
