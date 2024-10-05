from dotenv import load_dotenv

import os
import json
import hashlib
from typing import List, Dict
from langchain_community.document_loaders import FireCrawlLoader
from langchain_core.documents import Document
from llms import model4o
from e2b_runner import run_code_project
from schemas import IsBlogPostTechnical, BlogCodeRecipe, CodeRecipeDescriptions
from prompts import (
    extract_all_code_recipes_prompt,
    extract_code_metadata_prompt,
    extract_is_blog_post_technical_prompt,
)
import logging
import tiktoken

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
load_dotenv()

def num_tokens_from_string(string: str, model_name: str) -> int:
    """Calculate the number of tokens in a string based on the model's encoding.

    Args:
        string (str): The input text to be tokenized.
        model_name (str): The name of the OpenAI model to determine the encoding.

    Returns:
        int: The number of tokens in the input string.
    """
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def get_hashed_filename(url: str) -> str:
    """Generate a hashed filename for the given URL.

    Args:
        url (str): The URL to be hashed.

    Returns:
        str: The hashed filename.
    """
    return hashlib.md5(url.encode()).hexdigest() + ".json"

def load_docs_from_cache_or_scrape(
    url: str, cache_folder: str, model_name: str
) -> List[Document]:
    """Load documents from cache if available, otherwise scrape using FireCrawlLoader and save to cache.
    Adds token count as metadata to each document.

    Args:
        url (str): The URL to scrape.
        cache_folder (str): The folder to store cached JSON files.
        model_name (str): The name of the OpenAI model to determine the encoding.

    Returns:
        List[Document]: The loaded documents with token count metadata.
    """
    os.makedirs(cache_folder, exist_ok=True)
    hashed_filename = get_hashed_filename(url)
    cache_file_path = os.path.join(cache_folder, hashed_filename)

    if os.path.exists(cache_file_path):
        logger.info(f"Loading documents from cache: {cache_file_path}")
        with open(cache_file_path, "r") as f:
            raw_file_data = json.load(f)
            docs = [Document(**doc) for doc in raw_file_data]
    else:
        logger.info(f"Scraping documents from URL: {url}")
        loader = FireCrawlLoader(url=url, mode="scrape")
        docs = loader.load()
        with open(cache_file_path, "w") as f:
            json.dump([doc.dict() for doc in docs], f)

    for doc in docs:
        token_count = num_tokens_from_string(doc.page_content, model_name)
        doc.metadata["token_count"] = token_count

    return docs

def update_env_file(blog_code_recipe: BlogCodeRecipe, env_content: str) -> None:
    """Update the .env file content in the blog code recipe with the provided environment content.

    Args:
        blog_code_recipe (BlogCodeRecipe): The blog code recipe containing the .env file.
        env_content (str): The environment content to update the .env file with.
    """
    env_dict: Dict[str, str] = dict(line.split("=") for line in env_content.strip().split("\n"))

    for code_file in blog_code_recipe.code:
        if code_file.filepath == ".env":
            env_lines = code_file.content.split("\n")
            updated_env_lines = []
            existing_keys = set()
            for line in env_lines:
                if line.strip() and "=" in line:
                    key, _ = line.split("=", 1)
                    existing_keys.add(key)
                    if key in env_dict:
                        updated_env_lines.append(f"{key}={env_dict[key]}")
                    else:
                        updated_env_lines.append(line)
                else:
                    updated_env_lines.append(line)

            for key, value in env_dict.items():
                if key not in existing_keys:
                    updated_env_lines.append(f"{key}={value}")

            code_file.content = "\n".join(updated_env_lines)
            break

def get_blog_code_recipes_with_ai(blog_post_content: str) -> List[BlogCodeRecipe]:
    """Extract code recipes from a blog post using AI models.

    Args:
        blog_post_content (str): The content of the blog post.

    Returns:
        List[BlogCodeRecipe]: The extracted code recipes.
    """
    extract_tech_deets_model = model4o.with_structured_output(IsBlogPostTechnical)
    extract_code_deets_model = model4o.with_structured_output(BlogCodeRecipe)
    first_pass_details_chain = (
        extract_is_blog_post_technical_prompt | extract_tech_deets_model
    )

    extract_code_recipes_chain = extract_code_metadata_prompt | extract_code_deets_model

    _ = first_pass_details_chain.invoke({"blog_post": blog_post_content})

    extract_code_recipe_description_chain = (
        extract_all_code_recipes_prompt
        | model4o.with_structured_output(CodeRecipeDescriptions)
    )
    code_recipe_descriptions = extract_code_recipe_description_chain.invoke(
        {"blog_post": blog_post_content}
    )

    code_recipe_extraction_inputs = [
        {
            "code_recipe_description": str(code_recipe_description),
            "blog_post": blog_post_content,
        }
        for code_recipe_description in code_recipe_descriptions.recipes
    ]
    code_details = extract_code_recipes_chain.batch(code_recipe_extraction_inputs)

    return code_details

def check_code_recipe_with_e2b(input_code_recipe: BlogCodeRecipe, env_content: str) -> None:
    """Check the code recipe by running it with e2b.

    Args:
        input_code_recipe (BlogCodeRecipe): The code recipe to check.
        env_content (str): The environment content to update the .env file with.
    """
    update_env_file(input_code_recipe, env_content)
    logger.info(f"Running code project: {input_code_recipe.title}")
    result = run_code_project(input_code_recipe)
    logger.info(f"Exit Code: {result.exit_code}")
    logger.info(f"Standard Output: {result.stdout}")
    logger.info(f"Standard Error: {result.stderr}")
    logger.info("\n" * 3)
