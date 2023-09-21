from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models.accounts import User
from .models.project import Project, Issue, Comment


# TODO:  order the Contributors by project_name and by role: author first

admin.site.register(User, UserAdmin)
admin.site.register(Project)
# admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
