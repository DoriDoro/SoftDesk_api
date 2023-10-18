from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthor(BasePermission):
    """Object-level permission to only allow authors to edit and delete an object"""

    message = "You have to be the author to update or delete."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.author == request.user


class IsProjectAuthor(BasePermission):
    """Object-level permission to only allow authors to edit and delete an object"""

    message = "You have to be the author to update or delete."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        # obj is UserModel -> UserModel.project_author
        #   where project_author is the related_name to UserModel
        project_author = obj.project_author
        return project_author.author == request.user

        # if obj.project_author.author == request.user:
        #     return True
        # return False


class IsProjectContributor(BasePermission):
    """Permission to add other contributors when request.user is contributor of project"""

    message = "You are no contributor of this project."

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        project_contributor = obj.project_contributor
        return request.user in project_contributor


# class IsProjectContributor(BasePermission):
#     """Permission to have a Read-Only-Permission"""
#
#     message = "You have a ready only permission."
#
#     def has_permission(self, request, view):
#         return request.user.project_contributor.filter(pk=request.data["user"]).exists()
