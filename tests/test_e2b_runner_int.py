import os
import pytest
from dotenv import load_dotenv
from blogchecker.app.e2b_runner import run_code_project
from blogchecker.app.schemas import BlogCodeRecipe, LanguageEnum, CodeFile

# Load environment variables
load_dotenv()


@pytest.fixture
def e2b_api_key():
    return os.getenv("E2B_API_KEY")


@pytest.mark.integration
def test_run_python_project(e2b_api_key):
    print(e2b_api_key)
    python_project = BlogCodeRecipe(
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

    result = run_code_project(python_project)

    assert result.exit_code == 0
    assert "Hello from Python!" in result.stdout
    assert result.stderr == ""


@pytest.mark.integration
def test_run_python_yaml_project(e2b_api_key):
    python_yaml_project = BlogCodeRecipe(
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
                language=LanguageEnum.PYTHON,
            ),
            CodeFile(
                filepath="requirements.txt",
                content="pyyaml\nrequests",
                language=LanguageEnum.OTHER,
            ),
        ],
    )

    result = run_code_project(python_yaml_project)

    assert result.exit_code == 0
    assert "3.0.0" in result.stdout
    assert result.stderr == ""


@pytest.mark.integration
def test_run_project_with_error(e2b_api_key):
    error_project = BlogCodeRecipe(
        title="Error Test",
        published_at="2023-01-01T00:00:00Z",
        description="A test with an error",
        language=LanguageEnum.PYTHON,
        success_criteria="Test fails",
        entrypoint="main.py",
        code=[
            CodeFile(
                filepath="main.py",
                content="raise Exception('Intentional error')",
                language=LanguageEnum.PYTHON,
            ),
            CodeFile(
                filepath="requirements.txt", content="", language=LanguageEnum.OTHER
            ),
        ],
    )

    result = run_code_project(error_project)

    assert result.exit_code != 0
    assert "Intentional error" in result.stderr


@pytest.mark.integration
def test_run_nodejs_project(e2b_api_key):
    nodejs_project = BlogCodeRecipe(
        title="Node.js Test",
        published_at="2023-01-01T00:00:00Z",
        description="A test with Node.js code",
        language=LanguageEnum.JAVASCRIPT,
        success_criteria="Test passes",
        entrypoint="index.js",
        code=[
            CodeFile(
                filepath="index.js",
                content="""
console.log('Starting Node.js test');
const fs = require('fs');

try {
    fs.writeFileSync('test.txt', 'Hello from Node.js!');
    const content = fs.readFileSync('test.txt', 'utf-8');
    console.log(content);
    console.log('File operations successful');
} catch (error) {
    console.error('Error:', error.message);
}
""",
                language=LanguageEnum.JAVASCRIPT,
            ),
            CodeFile(
                filepath="package.json",
                content='{"name": "nodejs-test", "version": "1.0.0"}',
                language=LanguageEnum.OTHER,
            ),
        ],
    )

    result = run_code_project(nodejs_project)

    assert result.exit_code == 0
    assert "Starting Node.js test" in result.stdout
    assert "Hello from Node.js!" in result.stdout
    assert "File operations successful" in result.stdout
    assert result.stderr == ""
