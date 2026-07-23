# src/ml_agent/cli.py
import typer
from pathlib import Path
from typing import Optional
import structlog
from ml_agent.core.config import Config
from ml_agent.core.logger import setup_logging
from ml_agent.auth.manager import AuthManager
from ml_agent.providers.registry import ProviderRegistry

app = typer.Typer(
    name="ml-agent",
    help="Multi-provider ML workflow framework"
)

def get_config() -> Config:
    """Get or create configuration."""
    config = Config()
    config.ensure_directories()
    return config

@app.command()
def list_providers():
    """List available LLM providers."""
    config = get_config()
    setup_logging(config.log_level, config.log_dir)
    logger = structlog.get_logger(__name__)

    providers = ProviderRegistry.list_available()
    typer.echo("Available providers:")
    for provider in providers:
        typer.echo(f"  • {provider}")

    logger.info("Listed providers", count=len(providers))

@app.command()
def validate_auth(
    provider: str = typer.Option(..., help="Provider name"),
    api_key: Optional[str] = typer.Option(None, help="API key (or use env/auth.json)"),
):
    """Validate credentials for a provider."""
    config = get_config()
    setup_logging(config.log_level, config.log_dir)
    logger = structlog.get_logger(__name__)

    auth_manager = AuthManager(cli_api_key=api_key)

    try:
        key = auth_manager.get_api_key(provider)
        provider_instance = ProviderRegistry.get(provider, key)

        if provider_instance.validate_credentials():
            typer.secho(f"✓ {provider} credentials valid!", fg=typer.colors.GREEN)
            logger.info("Auth valid", provider=provider)
        else:
            typer.secho(f"✗ {provider} credentials invalid!", fg=typer.colors.RED)
            logger.warning("Auth invalid", provider=provider)

    except Exception as e:
        typer.secho(f"✗ Error: {e}", fg=typer.colors.RED)
        logger.error("Auth error", provider=provider, error=str(e))
        raise typer.Exit(1)

# Note: login and status commands moved to login.py script
# Use: python3 login.py claude (or openai, status)


@app.command()
def version():
    """Show version."""
    from ml_agent import __version__
    typer.echo(f"ml-agent {__version__}")

@app.callback()
def main(
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging"),
):
    """ML Agent Framework - Multi-provider ML workflows."""
    # Debug logging can be enabled later via LOG_LEVEL env var
    pass

if __name__ == "__main__":
    app()
