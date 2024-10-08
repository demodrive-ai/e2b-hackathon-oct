# Generated by Django 5.1.1 on 2024-10-05 19:51

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Blog",
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
                ("title", models.CharField(max_length=255)),
                ("content", models.TextField()),
                (
                    "language",
                    models.CharField(
                        choices=[
                            ("python", "Python"),
                            ("javascript", "JavaScript"),
                            ("typescript", "TypeScript"),
                        ],
                        max_length=20,
                    ),
                ),
                ("is_valid", models.BooleanField(default=False)),
                ("is_public", models.BooleanField(default=False)),
                ("last_check_timestamp", models.DateTimeField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "Blog Post",
                "verbose_name_plural": "Blog Posts",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="E2BRunOutput",
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
                ("title", models.CharField(max_length=255)),
                ("published_at", models.DateTimeField()),
                ("description", models.TextField()),
                ("language", models.CharField(max_length=20)),
                ("success_criteria", models.TextField()),
                ("entrypoint", models.CharField(max_length=255)),
                ("code_content", models.JSONField()),
                ("stdout", models.TextField(blank=True)),
                ("stderr", models.TextField(blank=True)),
                ("exit_code", models.IntegerField(null=True)),
                ("error", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "blog_post",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="e2b_runs",
                        to="blogchecker.blog",
                    ),
                ),
            ],
            options={
                "verbose_name": "E2B Run Output",
                "verbose_name_plural": "E2B Run Outputs",
                "ordering": ["-created_at"],
            },
        ),
    ]
