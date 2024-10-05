import pytest
from unittest.mock import patch, MagicMock
from app.e2b_runner import run_code_project
from app.schema import BlogCodeProject, LanguageEnum, CodeFile
from e2b_code_interpreter import ProcessOutput


@pytest.fixture
def mock_code_interpreter():
    with patch("app.e2b_runner.CodeInterpreter") as mock:
        yield mock


@pytest.fixture
def sample_blog_code_project():
    return BlogCodeProject(
        title="Test Project",
        published_at="2023-01-01T00:00:00Z",
        description="A test project",
        language=LanguageEnum.PYTHON,
        success_criteria="Test passes",
        entrypoint="main.py",
        code=[
            CodeFile(filepath="main.py", content="print('Hello, World!')"),
            CodeFile(filepath="requirements.txt", content="pytest==7.3.1"),
        ],
    )


def test_run_code_project_python(mock_code_interpreter, sample_blog_code_project):
    mock_instance = MagicMock()
    mock_code_interpreter.return_value.__enter__.return_value = mock_instance

    expected_output = ProcessOutput(stdout="Hello, World!\n", stderr="", exit_code=0)
    mock_instance.process.start_and_wait.return_value = expected_output

    result = run_code_project(sample_blog_code_project)

    assert result == expected_output
    mock_instance.filesystem.write.assert_called_with(
        "/opt/app/main.py", "print('Hello, World!')"
    )
    mock_instance.process.start_and_wait.assert_any_call(
        "cd /opt/app && pip install -r requirements.txt"
    )
    mock_instance.process.start_and_wait.assert_called_with(
        "cd /opt/app && python main.py"
    )


def test_run_code_project_javascript(mock_code_interpreter):
    js_project = BlogCodeProject(
        title="JS Test",
        published_at="2023-01-01T00:00:00Z",
        description="A JavaScript test",
        language=LanguageEnum.JAVASCRIPT,
        success_criteria="Test passes",
        entrypoint="index.js",
        code=[
            CodeFile(filepath="index.js", content="console.log('Hello, World!');"),
            CodeFile(filepath="package.json", content='{"dependencies":{}}'),
        ],
    )

    mock_instance = MagicMock()
    mock_code_interpreter.return_value.__enter__.return_value = mock_instance

    expected_output = ProcessOutput(stdout="Hello, World!\n", stderr="", exit_code=0)
    mock_instance.process.start_and_wait.return_value = expected_output

    result = run_code_project(js_project)

    assert result == expected_output
    mock_instance.filesystem.write.assert_called_with(
        "/opt/app/index.js", "console.log('Hello, World!');"
    )
    mock_instance.process.start_and_wait.assert_any_call("cd /opt/app && npm install")
    mock_instance.process.start_and_wait.assert_called_with(
        "cd /opt/app && javascript index.js"
    )


def test_run_code_project_typescript(mock_code_interpreter):
    ts_project = BlogCodeProject(
        title="TS Test",
        published_at="2023-01-01T00:00:00Z",
        description="A TypeScript test",
        language=LanguageEnum.TYPESCRIPT,
        success_criteria="Test passes",
        entrypoint="index.ts",
        code=[
            CodeFile(filepath="index.ts", content="console.log('Hello, World!');"),
            CodeFile(filepath="package.json", content='{"dependencies":{}}'),
        ],
    )

    mock_instance = MagicMock()
    mock_code_interpreter.return_value.__enter__.return_value = mock_instance

    expected_output = ProcessOutput(stdout="Hello, World!\n", stderr="", exit_code=0)
    mock_instance.process.start_and_wait.return_value = expected_output

    result = run_code_project(ts_project)

    assert result == expected_output
    mock_instance.filesystem.write.assert_called_with(
        "/opt/app/index.ts", "console.log('Hello, World!');"
    )
    mock_instance.process.start_and_wait.assert_any_call("cd /opt/app && npm install")
    mock_instance.process.start_and_wait.assert_called_with(
        "cd /opt/app && typescript index.ts"
    )


def test_run_code_project_error(mock_code_interpreter, sample_blog_code_project):
    mock_instance = MagicMock()
    mock_code_interpreter.return_value.__enter__.return_value = mock_instance

    expected_output = ProcessOutput(stdout="", stderr="Error occurred", exit_code=1)
    mock_instance.process.start_and_wait.return_value = expected_output

    result = run_code_project(sample_blog_code_project)

    assert result == expected_output
    assert result.exit_code == 1
    assert "Error occurred" in result.stderr
