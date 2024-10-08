from rest_framework import viewsets, status, serializers
from datetime import timezone, datetime
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import E2BRunOutput, BlogCodeRecipe, Blog
from app.blog_checker_main import (
    load_docs_from_cache_or_scrape,
    get_blog_code_recipes_with_ai,
    get_env_keys_as_string,
    check_code_recipe_with_e2b,
)
import logging
import os
from e2b_code_interpreter import CodeInterpreter

logger = logging.getLogger(__name__)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class E2BRunOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = E2BRunOutput
        fields = "__all__"


class BlogCodeRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCodeRecipe
        fields = "__all__"


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    def retrieve(self, request, *args, **kwargs):
        blog = self.get_object()

        blog_code_recipes = BlogCodeRecipe.objects.filter(blog=blog)

        e2b_run_outputs = E2BRunOutput.objects.filter(
            blog_code_recipe__in=blog_code_recipes
        ).order_by("exit_code")

        result = BlogSerializer(blog).data
        result["e2b_run_outputs"] = [
            E2BRunOutputSerializer(e2b_run_output).data
            for e2b_run_output in e2b_run_outputs
        ]
        result["blog_code_recipes"] = [
            BlogCodeRecipeSerializer(blog_code_recipe).data
            for blog_code_recipe in blog_code_recipes
        ]

        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=["post"], url_path="analyze")
    def analyze(self, request, *args, **kwargs):
        url = request.data.get("url")

        blog = Blog.objects.get(url=url)
        if not blog.url:
            raise serializers.ValidationError("Blog URL is required")

        blog_loaded_docs = load_docs_from_cache_or_scrape(blog.url)
        blog_content = blog_loaded_docs[0].page_content
        code_recipes = get_blog_code_recipes_with_ai(blog_post_content=blog_content)
        all_succeeded = True
        code_interpreter = CodeInterpreter(api_key=os.getenv("E2B_API_KEY"))
        for code_recipe in code_recipes:
            try:
                blog_code_recipe = BlogCodeRecipe.objects.create(
                    title=code_recipe.title,
                    published_at=datetime.now(tz=timezone.utc),
                    description=code_recipe.description,
                    language=code_recipe.language,
                    code_content=[
                        code_file.model_dump() for code_file in code_recipe.code
                    ],
                    success_criteria=code_recipe.success_criteria,
                    entrypoint=code_recipe.entrypoint,
                    blog=blog,
                )
                logger.info(f"Blog code recipe {blog_code_recipe}")
                logger.info(f"Stored {code_recipe.title}")
                env_content = get_env_keys_as_string(
                    "/Users/selvampalanimalai/projects/e2b-hackathon-oct/.env"
                )
                e2b_output = check_code_recipe_with_e2b(
                    code_recipe,
                    env_content=env_content,
                    code_interpreter=code_interpreter,
                )
                E2BRunOutput.objects.get_or_create(
                    stdout=e2b_output.stdout,
                    stderr=e2b_output.stderr,
                    exit_code=e2b_output.exit_code,
                    code_interpreter_hostname=e2b_output.code_interpreter_hostname,
                    error=e2b_output.error,
                    blog_code_recipe=blog_code_recipe,
                )
                if e2b_output.exit_code != 0:
                    all_succeeded = False

            except Exception as e:
                logger.error(f"Skipped {code_recipe.title} with error {e}")

            blog.is_valid = all_succeeded
            blog.is_analyzed = True
            blog.save()

        return Response({"status": "success", "output": BlogSerializer(blog).data})


class BlogCodeRecipeViewSet(viewsets.ModelViewSet):
    queryset = BlogCodeRecipe.objects.all()
    serializer_class = BlogCodeRecipeSerializer

    @action(detail=True, methods=["post"], url_path="rerun")
    def rerun(self, request, *args, **kwargs):
        blog_code_recipe = self.get_object()
        e2b_output = check_code_recipe_with_e2b(
            blog_code_recipe,
            env_content=get_env_keys_as_string(
                "/Users/selvampalanimalai/projects/e2b-hackathon-oct/.env"
            ),
        )
        E2BRunOutput.objects.get_or_create(
            stdout=e2b_output.stdout,
            stderr=e2b_output.stderr,
            exit_code=e2b_output.exit_code,
            code_interpreter_hostname=e2b_output.code_interpreter_hostname,
            error=e2b_output.error,
            blog_code_recipe=blog_code_recipe,
        )
        return Response({"status": "success"})
