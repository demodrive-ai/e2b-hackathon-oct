# Generated by Django 5.1.1 on 2024-10-05 21:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("blogchecker", "0002_remove_blog_author_remove_blog_content_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="e2brunoutput",
            old_name="blog_post",
            new_name="blog",
        ),
        migrations.CreateModel(
            name="BlogCodeRecipe",
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
                ("code_content", models.JSONField()),
                ("success_criteria", models.TextField()),
                ("entrypoint", models.CharField(max_length=255)),
                (
                    "blog",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="code_recipes",
                        to="blogchecker.blog",
                    ),
                ),
            ],
        ),
    ]