from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from enum import Enum

class LanguageEnum(str, Enum):
        python = "python"
        javascript = "javascript"
        typescript = "typescript"
        other = "other"

class Code(BaseModel):
    filepath: str = Field(..., description="The full path to the file containing the code.")
    content: str = Field(..., description="The code of the technical blog post.")
    

class BlogCodeProject(BaseModel):
    title: str = Field(..., description="The title of the technical blog post.")
    published_at: datetime = Field(..., description="The published at of the technical blog post.")
    description: str = Field(..., description="The description of the technical blog post.")
    code: str = Field(..., description="The code of the technical blog post.")
    language: LanguageEnum = Field(..., description="The language of the technical blog post.")
    success_criteria: str = Field(..., description="The success criteria of executing the technical blog post.")
