from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from enum import Enum


class LanguageEnum(str, Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    OTHER = "other"


class IsBlogPostTechnical(BaseModel):
    is_technical: bool = Field(..., description="Whether the blog post is technical.")
    is_code_recipe: bool = Field(
        ..., description="Whether the blog post is a code recipe."
    )
    language: LanguageEnum = Field(
        ..., description="The language of the technical blog post."
    )


class CodeFile(BaseModel):
    filepath: str = Field(
        ..., description="The full path to the file containing the code."
    )
    content: str = Field(..., description="The code of the technical blog post.")
    language: LanguageEnum = Field(..., description="The language of the file.")


class CodeRecipeDescription(BaseModel):
    title: str = Field(..., description="The title of the Code Recipe")
    description: str = Field(
        ...,
        description="Short description of the code recipe which is information dense, succinct and captures as much detail as possible in fewest words.",
    )

    def __str__(self):
        return f"### {self.title}\n\n{self.description}"


class CodeRecipeDescriptions(BaseModel):
    recipes: List[CodeRecipeDescription] = Field(
        ..., description="All the code recipes in the technical blog post"
    )

    def __str__(self):
        return "\n\n".join(str(recipe) for recipe in self.recipes)


class BlogCodeRecipeLLM(BaseModel):
    title: str = Field(..., description="The title of an individual code recipe")
    published_at: datetime = Field(
        ..., description="The published at of the technical blog post."
    )
    description: str = Field(
        ..., description="The description of the technical blog post."
    )
    language: LanguageEnum = Field(..., description="The language of the file.")
    code: List[CodeFile] = Field(
        ..., description="The code of the technical blog post."
    )
    success_criteria: str = Field(
        ..., description="The success criteria of executing the technical blog post."
    )
    entrypoint: str = Field(
        ..., description="The entrypoint of the technical blog post."
    )
