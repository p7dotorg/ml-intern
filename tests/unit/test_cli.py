# tests/unit/test_cli.py
from typer.testing import CliRunner
from ml_agent.cli import app

runner = CliRunner()

def test_list_providers():
    """Test list-providers command."""
    result = runner.invoke(app, ["list-providers"])
    assert result.exit_code == 0
    assert "claude" in result.stdout.lower()
    assert "openai" in result.stdout.lower()

def test_version():
    """Test version command."""
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "ml-agent" in result.stdout

def test_help():
    """Test help command."""
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Multi-provider" in result.stdout
