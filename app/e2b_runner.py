from e2b_code_interpreter import CodeInterpreter, ProcessOutput
from dotenv import load_dotenv
import os
from .schemas import BlogCodeRecipe, LanguageEnum

load_dotenv()

WORK_DIR = "/opt/"


def run_code_project(blog_code_recipe: BlogCodeRecipe) -> ProcessOutput:
    with CodeInterpreter(api_key=os.getenv("E2B_API_KEY")) as code_interpreter:
        for code in blog_code_recipe.code:
            print(code)
            print("Hostname", code_interpreter.get_hostname())
            r = code_interpreter.filesystem.write(
                f"{WORK_DIR}/{code.filepath}", code.content
            )
            print(r)

        print(code_interpreter.filesystem.list(WORK_DIR))

        if blog_code_recipe.language == LanguageEnum.PYTHON:
            code_interpreter.process.start_and_wait(
                f"cd {WORK_DIR} && pip install -r requirements.txt"
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
