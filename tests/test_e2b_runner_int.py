import os
import pytest
from dotenv import load_dotenv
from app.e2b_runner import run_code_project
from app.schema import BlogCodeProject, LanguageEnum, CodeFile

# Load environment variables
load_dotenv()


@pytest.fixture
def e2b_api_key():
    return os.getenv("E2B_API_KEY")


@pytest.mark.integration
def test_run_python_project(e2b_api_key):
    print(e2b_api_key)
    python_project = BlogCodeProject(
        title="Python Test",
        published_at="2023-01-01T00:00:00Z",
        description="A Python test",
        language=LanguageEnum.PYTHON,
        success_criteria="Test passes",
        entrypoint="main.py",
        code=[
            CodeFile(filepath="main.py", content="print('Hello from Python!')"),
            CodeFile(filepath="requirements.txt", content=""),
        ],
    )

    result = run_code_project(python_project)

    assert result.exit_code == 0
    assert "Hello from Python!" in result.stdout
    assert result.stderr == ""


@pytest.mark.integration
def test_run_python_yaml_project(e2b_api_key):
    python_yaml_project = BlogCodeProject(
        title="Python YAML Test",
        published_at="2023-01-01T00:00:00Z",
        description="A Python test to fetch and validate YAML",
        language=LanguageEnum.PYTHON,
        success_criteria="YAML is fetched and validated successfully",
        entrypoint="main.py",
        code=[
            CodeFile(
                filepath="main.py",
                content="""
import requests
import yaml

url = "https://raw.githubusercontent.com/OAI/OpenAPI-Specification/refs/heads/main/examples/v3.0/api-with-examples.yaml"
response = requests.get(url)
content = response.text

try:
    result = yaml.safe_load(content)
    print(result.get("openapi"))
    print("Valid YAML")
except yaml.YAMLError:
    print("Invalid YAML")
""",
            ),
            CodeFile(filepath="requirements.txt", content="pyyaml\nrequests"),
        ],
    )

    result = run_code_project(python_yaml_project)

    assert result.exit_code == 0
    assert "3.0.0" in result.stdout
    assert result.stderr == ""


# @pytest.mark.integration
# def test_run_javascript_project(e2b_api_key):
#     js_project = BlogCodeProject(
#         title="JavaScript Test",
#         published_at="2023-01-01T00:00:00Z",
#         description="A JavaScript test",
#         language=LanguageEnum.JAVASCRIPT,
#         success_criteria="Test passes",
#         entrypoint="index.js",
#         code=[
#             CodeFile(
#                 filepath="index.js", content="console.log('Hello from JavaScript!');"
#             ),
#             CodeFile(filepath="package.json", content='{"dependencies":{}}'),
#         ],
#     )

#     result = run_code_project(js_project)

#     assert result.exit_code == 0
#     assert "Hello from JavaScript!" in result.stdout
#     assert result.stderr == ""


# @pytest.mark.integration
# def test_run_typescript_project(e2b_api_key):
#     ts_project = BlogCodeProject(
#         title="TypeScript Test",
#         published_at="2023-01-01T00:00:00Z",
#         description="A TypeScript test",
#         language=LanguageEnum.TYPESCRIPT,
#         success_criteria="Test passes",
#         entrypoint="index.ts",
#         code=[
#             CodeFile(
#                 filepath="index.ts", content="console.log('Hello from TypeScript!');"
#             ),
#             CodeFile(
#                 filepath="package.json",
#                 content='{"dependencies":{"typescript":"^4.5.4"}}',
#             ),
#         ],
#     )

#     result = run_code_project(ts_project)

#     assert result.exit_code == 0
#     assert "Hello from TypeScript!" in result.stdout
#     assert result.stderr == ""


@pytest.mark.integration
def test_run_project_with_error(e2b_api_key):
    error_project = BlogCodeProject(
        title="Error Test",
        published_at="2023-01-01T00:00:00Z",
        description="A test with an error",
        language=LanguageEnum.PYTHON,
        success_criteria="Test fails",
        entrypoint="main.py",
        code=[
            CodeFile(
                filepath="main.py", content="raise Exception('Intentional error')"
            ),
            CodeFile(filepath="requirements.txt", content=""),
        ],
    )

    result = run_code_project(error_project)

    assert result.exit_code != 0
    assert "Intentional error" in result.stderr
