from e2b_code_interpreter import CodeInterpreter, ProcessOutput
from dotenv import load_dotenv
from app.schemas import BlogCodeRecipeLLM, LanguageEnum

import logging

logger = logging.getLogger(__name__)

load_dotenv()

WORK_DIR = "/home/user"


def run_code_project(
    blog_code_recipe: BlogCodeRecipeLLM, code_interpreter: CodeInterpreter
) -> ProcessOutput:
    logger.info("Hostname E2B", code_interpreter.get_hostname())
    for code in blog_code_recipe.code:
        logger.info("writing code file %s", code.model_dump_json())
        r = code_interpreter.filesystem.write(
            f"{WORK_DIR}/{code.filepath}", code.content
        )
        # logger.info("wrote code file %s", r)
    # if ".env" not in code_interpreter.filesystem.list(WORK_DIR):
    #     code_interpreter.filesystem.write(
    #         f"{WORK_DIR}/.env",
    #         "",
    #     )
    # logger.info("list files", code_interpreter.filesystem.list(WORK_DIR))

    if blog_code_recipe.language == LanguageEnum.PYTHON:
        code_interpreter.process.start_and_wait(
            f"cd {WORK_DIR} && export $(grep -v '^#' .env | xargs) && pip install -r requirements.txt"
        )
        ENTRYPOINT = f"python {blog_code_recipe.entrypoint}"
    elif blog_code_recipe.language == LanguageEnum.JAVASCRIPT:
        r = code_interpreter.process.start_and_wait(f"cd {WORK_DIR} && npm install")
        print("NPM Install", r)
        ENTRYPOINT = f"node {blog_code_recipe.entrypoint}"
    elif blog_code_recipe.language == LanguageEnum.TYPESCRIPT:
        r = code_interpreter.process.start_and_wait(f"cd {WORK_DIR} && npm install")
        print("NPM Install", r)
        ENTRYPOINT = f"npx ts-node {blog_code_recipe.entrypoint}"

    output: ProcessOutput = code_interpreter.process.start_and_wait(
        f"cd {WORK_DIR} && export $(grep -v '^#' .env | xargs) && {ENTRYPOINT}"
    )
    return output
