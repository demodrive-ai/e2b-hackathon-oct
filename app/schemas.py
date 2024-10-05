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
    is_code_recipe: bool = Field(..., description="Whether the blog post is a code recipe.")
    language: LanguageEnum = Field(..., description="The language of the technical blog post.")

class CodeFile(BaseModel):
    filepath: str = Field(..., description="The full path to the file containing the code.")
    content: str = Field(..., description="The code of the technical blog post.")
    language: LanguageEnum = Field(
        ..., description="The language of the file."
    )


class BlogCodeProject(BaseModel):
    title: str = Field(..., description="The title of the technical blog post.")
    published_at: datetime = Field(
        ..., description="The published at of the technical blog post."
    )
    description: str = Field(
        ..., description="The description of the technical blog post."
    )
    code: List[CodeFile] = Field(
        ..., description="The code of the technical blog post."
    )
    success_criteria: str = Field(
        ..., description="The success criteria of executing the technical blog post."
    )

    entrypoint: str = Field(
        ..., description="The entrypoint of the technical blog post."
    )
