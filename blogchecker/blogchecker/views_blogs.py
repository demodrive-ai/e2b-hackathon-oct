from rest_framework import viewsets
from datetime import timezone, datetime
from .models import Blog, E2BRunOutput, BlogCodeRecipe
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from app.e2b_runner import run_code_project
from app.schemas import BlogCodeRecipeLLM, LanguageEnum, CodeFile
from .models import E2BRunOutput, BlogCodeRecipe
from rest_framework import status
from app.blog_checker_main import (
    load_docs_from_cache_or_scrape,
    get_blog_code_recipes_with_ai,
)


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

        blog_code_recipes = BCR.objects.filter(blog=blog)

        e2b_run_outputs = E2BRunOutput.objects.filter(
            blog_code_recipe__in=blog_code_recipes
        )

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
        print(f"YAYA {blog}")
        if not blog.url:
            raise serializers.ValidationError("Blog URL is required")

        blog_loaded_docs = load_docs_from_cache_or_scrape(blog.url)
        blog_content = blog_loaded_docs[0].page_content
        print(blog_content)
        code_recipes = get_blog_code_recipes_with_ai(blog_post_content=blog_content)
        print(code_recipes)
        for code_recipe in code_recipes:
            BlogCodeRecipe.objects.get_or_create(
                title=code_recipe.title,
                published_at=datetime.now(tz=timezone.utc),
                description=code_recipe.description,
                language=code_recipe.language,
                code_content=code_recipe.model_dump_json(),
                success_criteria=code_recipe.success_criteria,
                entrypoint=code_recipe.entrypoint,
            )
        # call LLM loop to generate code recipes
        # loop through each code recipe, save it in DB and run it in e2b.
        # save the output for each code recipe.
        # if any recipe fails, respond with error to client.
        # if all pass, respond with success to client.

        code_recipe = BlogCodeRecipe(
            title="Python Test",
            published_at="2023-01-01T00:00:00Z",
            description="A Python test",
            language=LanguageEnum.PYTHON,
            success_criteria="Test passes",
            entrypoint="main.py",
            code=[
                CodeFile(
                    filepath="main.py",
                    content="print('Hello from Python!')",
                    language=LanguageEnum.PYTHON,
                ),
                CodeFile(
                    filepath="requirements.txt", content="", language=LanguageEnum.OTHER
                ),
            ],
        )

        # E2BRunOutput.objects.get_or_create(
        #     title=code_recipe.title,
        #     published_at=code_recipe.published_at,
        #     description=code_recipe.description,
        #     language=code_recipe.language,
        #     success_criteria=code_recipe.success_criteria,
        #     entrypoint=code_recipe.entrypoint,
        #     code=code_recipe.code,
        # )
        output = run_code_project(code_recipe)

        return Response({"status": "success", "output": output})
