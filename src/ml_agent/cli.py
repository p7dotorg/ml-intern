# src/ml_agent/cli.py
import json
import typer
from pathlib import Path
from typing import Optional
import structlog
from ml_agent.core.config import Config
from ml_agent.core.logger import setup_logging
from ml_agent.auth.manager import AuthManager
from ml_agent.auth.oauth import OAuthManager
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

@app.command()
def login(provider: str = typer.Option("claude", help="Provider (claude, openai)")):
    """Login to provider via OAuth (Claude Pro, ChatGPT Plus, etc)."""
    setup_logging()
    logger = structlog.get_logger(__name__)

    oauth_manager = OAuthManager()

    typer.echo(f"🔐 Logging in to {provider}...")
    typer.echo()

    if provider == "claude":
        typer.echo("Opening Claude.ai login in your browser...")
        typer.echo("1. Authenticate with your account")
        typer.echo("2. Grant permission to ml-agent")
        typer.echo("3. Copy the auth code here")
        typer.echo()

        auth_code = typer.prompt("Auth code")
        oauth_manager.authenticate_claude_oauth(auth_code)

        typer.secho("✓ Claude Pro login successful!", fg=typer.colors.GREEN)
        logger.info("Claude OAuth login successful")

    elif provider == "openai":
        typer.echo("Opening ChatGPT login in your browser...")
        typer.echo("1. Authenticate with your account")
        typer.echo("2. Grant permission to ml-agent")
        typer.echo("3. Copy the auth code here")
        typer.echo()

        auth_code = typer.prompt("Auth code")
        oauth_manager.authenticate_openai_oauth(auth_code)

        typer.secho("✓ ChatGPT Plus login successful!", fg=typer.colors.GREEN)
        logger.info("OpenAI OAuth login successful")

    else:
        typer.secho(f"✗ Unknown provider: {provider}", fg=typer.colors.RED)
        raise typer.Exit(1)


@app.command()
def status():
    """Show authentication status and subscriptions."""
    setup_logging()
    auth_manager = AuthManager()

    typer.echo("📊 Authentication Status")
    typer.echo()

    # List subscriptions
    subscriptions = auth_manager.list_subscriptions()

    if subscriptions:
        typer.echo("✓ Active Subscriptions:")
        for sub in subscriptions:
            typer.secho(
                f"  • {sub['subscription']} ({sub['provider']})",
                fg=typer.colors.GREEN,
            )
        typer.echo()
    else:
        typer.echo("No active subscriptions")
        typer.echo()

    # Check env vars
    import os

    api_keys = []
    if os.getenv("CLAUDE_API_KEY"):
        api_keys.append("CLAUDE_API_KEY")
    if os.getenv("OPENAI_API_KEY"):
        api_keys.append("OPENAI_API_KEY")

    if api_keys:
        typer.echo("✓ Environment Variables:")
        for key in api_keys:
            typer.echo(f"  • {key}")
        typer.echo()

    # Config file
    auth_file = Path.home() / ".ml-agent" / "auth.json"
    if auth_file.exists():
        typer.secho(f"✓ Auth file: {auth_file}", fg=typer.colors.BLUE)
    else:
        typer.echo(f"Auth file not found: {auth_file}")

    typer.echo()
    typer.echo("💡 To login:")
    typer.echo("  ml-agent login claude   # Claude Pro")
    typer.echo("  ml-agent login openai   # ChatGPT Plus")


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
