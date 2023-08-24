import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from softdesk import settings


class Project(models.Model):
    """Contributor creates project as author and assign other Contributor(s)"""

    # project_types for project
    BACKEND = "B"
    FRONTEND = "F"
    IOS = "I"
    ANDROID = "A"

    PROJECT_TYPES = [
        (BACKEND, "Back-end"),
        (FRONTEND, "Front-end"),
        (IOS, "iOS"),
        (ANDROID, "Android"),
    ]

    created_itme = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    name = models.CharField(max_length=100, verbose_name=_("name of project"))
    description = models.TextField(verbose_name=_("project description"))
    project_types = models.CharField(
        max_length=1, choices=PROJECT_TYPES, verbose_name=_("project types")
    )

    def __str__(self):
        return f"{self.name}"


class Contributor(models.Model):
    """Author or Contributor of Project(s), Issue(s) and Comment(s)
    Contributor(s) related to type
    """

    # types of contributor
    PROJECT = "P"
    ISSUE = "I"
    COMMENT = "C"

    # roles of contributor
    AUTHOR = "A"
    CONTRIBUTOR = "CO"

    TYPES = [(PROJECT, "Project"), (ISSUE, "Issue"), (COMMENT, "Comment")]

    ROLES = [(AUTHOR, "Author"), (CONTRIBUTOR, "Contributor")]

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="users",
        verbose_name=_("user"),
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="project",
        verbose_name=_("project"),
    )
    types = models.CharField(
        max_length=1, choices=TYPES, verbose_name=_("contributor type")
    )
    role = models.CharField(
        max_length=2, choices=ROLES, verbose_name=_("contributor role")
    )

    class Meta:
        unique_together = ["user", "project"]

    def __str__(self):
        return f"{self.user} <{self.role}>"


class Issue(models.Model):
    """Issue is related to a project, default is state is ToDo"""

    # tags for issue
    BUG = "B"
    FEATURE = "FE"
    TASK = "TA"

    # state for issue
    TODO = "TO"
    INPROGRESS = "I"
    FINISHED = "FI"

    # priority for issue
    LOW = "L"
    MEDIUM = "M"
    HIGH = "H"

    TAGS = [
        (BUG, "Bug"),
        (FEATURE, "Feature"),
        (TASK, "Task"),
    ]

    STATE = [
        (TODO, "ToDo"),
        (INPROGRESS, "In Progress"),
        (FINISHED, "Finished"),
    ]

    PRIORITY = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    ]

    created_itme = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    contributor = models.ForeignKey(
        to=Contributor,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="issue_contributors",
        verbose_name=_("issue contributor"),
    )
    name = models.CharField(max_length=100, verbose_name=_("name of issue"))
    description = models.TextField(verbose_name=_("issue description"))
    tag = models.CharField(max_length=2, choices=TAGS, verbose_name=_("issue tag"))
    state = models.CharField(
        max_length=2, choices=STATE, default=TODO, verbose_name=_("issue state")
    )
    priority = models.CharField(
        max_length=1, choices=PRIORITY, verbose_name=_("issue priority")
    )
    project = models.ForeignKey(
        to=Project,
        on_delete=models.CASCADE,
        related_name="projects",
        verbose_name=_("related project"),
    )

    def __str__(self):
        return (
            f"{self.name} | {self.tag}, {self.state}, {self.priority} | {self.project} "
        )


class Comment(models.Model):
    """Comment is related to an Issue"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_itme = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    contributor = models.ForeignKey(
        to=Contributor,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="comment_contributors",
        verbose_name=_("comment contributor"),
    )
    name = models.CharField(max_length=100, verbose_name=_("comment name"))
    description = models.TextField(verbose_name=_("comment body"))
    issue = models.ForeignKey(
        to=Issue,
        on_delete=models.CASCADE,
        related_name="issues",
        verbose_name=_("related issue"),
    )

    def __str__(self):
        return f"{self.name} | {self.issue}"
