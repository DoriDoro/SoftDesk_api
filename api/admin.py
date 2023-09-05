from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models.accounts import User, Contributor
from .models.project import Project, Issue, Comment


admin.site.register(User, UserAdmin)
admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
admin.site.register(Comment)
