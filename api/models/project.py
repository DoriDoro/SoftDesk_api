import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


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

    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    name = models.CharField(max_length=100, verbose_name=_("name of project"))
    description = models.TextField(verbose_name=_("project description"))
    project_type = models.CharField(
        max_length=1, choices=PROJECT_TYPES, verbose_name=_("project type")
    )

    def __str__(self):
        return f"{self.name}"


class Issue(models.Model):
    """Issue is related to a project, default is state is ToDo"""

    # tags for issue
    BUG = "B"
    FEATURE = "FE"
    TASK = "TA"

    # state for issue
    TODO = "TO"
    IN_PROGRESS = "I"
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
        (IN_PROGRESS, "In Progress"),
        (FINISHED, "Finished"),
    ]

    PRIORITY = [
        (LOW, "Low"),
        (MEDIUM, "Medium"),
        (HIGH, "High"),
    ]

    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    author = models.ForeignKey(
        "api.Contributor",
        on_delete=models.CASCADE,
        related_name="issue_authors",
        blank=True,
        verbose_name=_("issue author"),
    )
    assigned_to = models.ForeignKey(
        "api.Contributor",
        on_delete=models.CASCADE,
        related_name="issue_contributors",
        null=True,
        blank=True,
        verbose_name=_("issue assigned to"),
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
        "api.Project",
        on_delete=models.CASCADE,
        related_name="issues",
        blank=True,
        verbose_name=_("related project"),
    )

    def __str__(self):
        return (
            f"{self.name} | {self.tag}, {self.state}, {self.priority} | {self.project} "
        )


class Comment(models.Model):
    """Comment is related to an Issue"""

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_time = models.DateTimeField(auto_now_add=True, verbose_name=_("created on"))
    author = models.ForeignKey(
        "api.Contributor",
        on_delete=models.CASCADE,
        related_name="comment_authors",
        blank=True,
        verbose_name=_("comment author"),
    )
    name = models.CharField(max_length=100, verbose_name=_("comment name"))
    description = models.TextField(verbose_name=_("comment body"))
    issue = models.ForeignKey(
        "api.Issue",
        on_delete=models.CASCADE,
        related_name="comments",
        blank=True,
        verbose_name=_("related issue"),
    )

    def __str__(self):
        return f"{self.name} | {self.issue}"
