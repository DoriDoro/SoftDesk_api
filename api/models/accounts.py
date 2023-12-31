from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(
        default=15, validators=[MinValueValidator(15)], verbose_name=_("age")
    )
    can_be_contacted = models.BooleanField(verbose_name=_("contact consent"))
    can_data_be_shared = models.BooleanField(verbose_name=_("share consent"))

    def __str__(self):
        return self.username
