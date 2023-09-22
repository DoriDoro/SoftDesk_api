from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .models.project import Project, Issue, Comment

UserModel = get_user_model()

# TODO:  order the Contributors by project_name and by role: author first


# class CustomUserAdmin(UserAdmin):
#     """Add custom attributes/fields to the Admin panel"""
#
#     # The fields to be used in displaying the User model
#     list_display = ["username", "can_be_contacted", "can_data_be_shared"]
#
#     fieldsets = [
#         (
#             "Additional Fields",
#             {"fields": ["age", "can_be_contacted", "can_data_be_shared", "project"]},
#         ),
#     ]
#     add_fieldsets = [
#         (None, {"fields": ["username", "password1", "password2"]}),
#         (
#             "Additional Fields",
#             {"fields": ["age", "can_be_contacted", "can_data_be_shared"]},
#         ),
#     ]


admin.site.register(UserModel, UserAdmin)
admin.site.register(Project)
admin.site.register(Issue)
admin.site.register(Comment)
