from rest_framework import viewsets
from .models import Blog, E2BRunOutput
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from app.e2b_runner import run_code_project
from app.schemas import BlogCodeRecipe, LanguageEnum, CodeFile


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer

    @action(detail=False, methods=["post"], url_path="analyze")
    def analyze(self, request, *args, **kwargs):
        url = request.data.get("url")
        blog = Blog.objects.get(url=url)
        print(blog)
        if not blog.url:
            raise serializers.ValidationError("Blog URL is required")

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

        E2BRunOutput.objects.get_or_create(
            title=code_recipe.title,
            published_at=code_recipe.published_at,
            description=code_recipe.description,
            language=code_recipe.language,
            success_criteria=code_recipe.success_criteria,
            entrypoint=code_recipe.entrypoint,
            code=code_recipe.code,
        )
        output = run_code_project(code_recipe)

        return Response({"status": "success", "output": output})
