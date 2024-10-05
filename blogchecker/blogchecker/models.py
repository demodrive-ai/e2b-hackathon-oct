from django.db import models
from django.contrib.postgres.fields import JSONField
from django.utils import timezone


class BlogPost(models.Model):
    LANGUAGE_CHOICES = [
        ("python", "Python"),
        ("javascript", "JavaScript"),
        ("typescript", "TypeScript"),
        # Add more language choices as needed
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    is_valid = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    last_check_timestamp = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"


class E2BRunOutput(models.Model):
    # BlogCodeProject fields
    title = models.CharField(max_length=255)
    published_at = models.DateTimeField()
    description = models.TextField()
    language = models.CharField(max_length=20)
    success_criteria = models.TextField()
    entrypoint = models.CharField(max_length=255)

    # Code content (stored as JSON)
    code_content = JSONField()

    # ProcessOutput fields
    stdout = models.TextField(blank=True)
    stderr = models.TextField(blank=True)
    exit_code = models.IntegerField(null=True)
    error = models.BooleanField(default=False)

    # Metadata
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"E2B Run: {self.title} ({self.created_at})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "E2B Run Output"
        verbose_name_plural = "E2B Run Outputs"
