from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from softdesk import settings


class User(AbstractUser):
    """create User instance with additional attributes"""

    age = models.PositiveSmallIntegerField(
        default=15, validators=[MinValueValidator(15)], verbose_name=_("age")
    )
    can_be_contacted = models.BooleanField(verbose_name=_("contact consent"))
    can_data_be_shared = models.BooleanField(verbose_name=_("share consent"))

    def __str__(self):
        return self.username


# class Contributor(models.Model):
#     """Author or Contributor of Project(s), Issue(s) and Comment(s)
#     Contributor(s) related to type
#     """
#
#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="contributors",
#         verbose_name=_("user"),
#     )
#     project = models.ForeignKey(
#         "api.Project",
#         on_delete=models.CASCADE,
#         related_name="project_contributors",
#         blank=True,
#         verbose_name=_("project"),
#     )
#
#     class Meta:
#         unique_together = ["user", "project"]
#
#     def __str__(self):
#         return f"{self.user}  | {self.project}"
