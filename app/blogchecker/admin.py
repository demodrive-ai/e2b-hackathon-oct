from django.contrib import admin

from django.db import models
from jsoneditor.forms import JSONEditor

from .models import E2BRunOutput, Blog, BlogCodeRecipe


class BlogCodeRecipeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "published_at",
        "description",
        "language",
        "success_criteria",
        "entrypoint",
        "blog",
    )
    list_filter = ["blog"]
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditor},
    }


class E2BRunOutputAdmin(admin.ModelAdmin):
    list_display = (
        "blog",
        "blog_code_recipe",
        "exit_code",
        "stdout",
        "stderr",
    )
    list_filter = ["blog_code_recipe__blog"]
    formfield_overrides = {
        models.JSONField: {"widget": JSONEditor},
    }

    def blog(self, obj):
        return obj.blog_code_recipe.blog if obj.blog_code_recipe else None

    blog.short_description = "Blog"


admin.site.register(E2BRunOutput, E2BRunOutputAdmin)
admin.site.register(Blog)
admin.site.register(BlogCodeRecipe, BlogCodeRecipeAdmin)
