# Generated by Django 4.2.5 on 2023-09-22 07:44

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "A user with that username already exists."
                        },
                        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.",
                        max_length=150,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="username",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="first name"
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        blank=True, max_length=150, verbose_name="last name"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        blank=True, max_length=254, verbose_name="email address"
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Designates whether this user should be treated as active. Unselect this instead of deleting accounts.",
                        verbose_name="active",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "age",
                    models.PositiveSmallIntegerField(
                        default=15,
                        validators=[django.core.validators.MinValueValidator(15)],
                        verbose_name="age",
                    ),
                ),
                (
                    "can_be_contacted",
                    models.BooleanField(verbose_name="contact consent"),
                ),
                (
                    "can_data_be_shared",
                    models.BooleanField(verbose_name="share consent"),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
            ],
            options={
                "verbose_name": "user",
                "verbose_name_plural": "users",
                "abstract": False,
            },
            managers=[
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="created on"),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="name of project"),
                ),
                ("description", models.TextField(verbose_name="project description")),
                (
                    "project_type",
                    models.CharField(
                        choices=[
                            ("B", "Back-end"),
                            ("F", "Front-end"),
                            ("I", "iOS"),
                            ("A", "Android"),
                        ],
                        max_length=1,
                        verbose_name="project type",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="project_author",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="project author",
                    ),
                ),
                (
                    "contributors",
                    models.ManyToManyField(
                        blank=True,
                        related_name="project_contributor",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="project contributors",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Issue",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="created on"),
                ),
                (
                    "name",
                    models.CharField(max_length=100, verbose_name="name of issue"),
                ),
                ("description", models.TextField(verbose_name="issue description")),
                (
                    "tag",
                    models.CharField(
                        choices=[("B", "Bug"), ("FE", "Feature"), ("TA", "Task")],
                        max_length=2,
                        verbose_name="issue tag",
                    ),
                ),
                (
                    "state",
                    models.CharField(
                        choices=[
                            ("TO", "ToDo"),
                            ("I", "In Progress"),
                            ("FI", "Finished"),
                        ],
                        default="TO",
                        max_length=2,
                        verbose_name="issue state",
                    ),
                ),
                (
                    "priority",
                    models.CharField(
                        choices=[("L", "Low"), ("M", "Medium"), ("H", "High")],
                        max_length=1,
                        verbose_name="issue priority",
                    ),
                ),
                (
                    "assigned_to",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issue_contributors",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="issue assigned to",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issue_authors",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="issue author",
                    ),
                ),
                (
                    "project",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="issues",
                        to="api.project",
                        verbose_name="related project",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, editable=False)),
                (
                    "created_time",
                    models.DateTimeField(auto_now_add=True, verbose_name="created on"),
                ),
                ("name", models.CharField(max_length=100, verbose_name="comment name")),
                ("description", models.TextField(verbose_name="comment body")),
                (
                    "issue_url",
                    models.URLField(blank=True, verbose_name="url verse an issue"),
                ),
                (
                    "author",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comment_authors",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="comment author",
                    ),
                ),
                (
                    "issue",
                    models.ForeignKey(
                        blank=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to="api.issue",
                        verbose_name="related issue",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="user",
            name="project",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="api.project",
                verbose_name="project user",
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="user_permissions",
            field=models.ManyToManyField(
                blank=True,
                help_text="Specific permissions for this user.",
                related_name="user_set",
                related_query_name="user",
                to="auth.permission",
                verbose_name="user permissions",
            ),
        ),
    ]
