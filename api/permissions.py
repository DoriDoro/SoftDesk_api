from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorPermission(BasePermission):
    """Object-level permission to only allow authors to edit and delete it"""

    message = "You have to be the author to update or delete."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsProjectContributorPermission(BasePermission):
    """Permission to have Read Only permission"""

    message = "You have a ready only permission."

    def has_permission(self, request, view):
        return request.user.projects.fiter(pk=request.data["project_pk"]).exists()
