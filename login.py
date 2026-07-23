#!/usr/bin/env python3
"""
ML Agent OAuth Login
Authenticate with Claude Pro, ChatGPT Plus, or other subscriptions.

Usage:
  python3 login.py claude    # Login to Claude Pro
  python3 login.py openai    # Login to ChatGPT Plus
  python3 login.py status    # Show authentication status
"""

import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ml_agent.auth.oauth import OAuthManager
from ml_agent.auth.oauth_server import oauth_login_flow
from ml_agent.auth.manager import AuthManager


def show_status():
    """Show authentication status."""
    print("📊 Authentication Status\n")

    auth_manager = AuthManager()
    subscriptions = auth_manager.list_subscriptions()

    if subscriptions:
        print("✓ Active Subscriptions:")
        for sub in subscriptions:
            print(f"  • {sub['subscription']} ({sub['provider']})")
        print()
    else:
        print("No active subscriptions\n")

    # Check env vars
    import os

    api_keys = []
    if os.getenv("CLAUDE_API_KEY"):
        api_keys.append("CLAUDE_API_KEY")
    if os.getenv("OPENAI_API_KEY"):
        api_keys.append("OPENAI_API_KEY")

    if api_keys:
        print("✓ Environment Variables:")
        for key in api_keys:
            print(f"  • {key}")
        print()

    # Config file
    auth_file = Path.home() / ".ml-agent" / "auth.json"
    if auth_file.exists():
        print(f"✓ Auth file: {auth_file}\n")
    else:
        print(f"Auth file not found: {auth_file}\n")

    print("💡 To login:")
    print("  python3 login.py claude   # Claude Pro")
    print("  python3 login.py openai   # ChatGPT Plus")


def login_claude():
    """Login to Claude Pro via OAuth."""
    oauth_manager = OAuthManager()

    # OAuth URL (in real app, would be from Anthropic)
    oauth_url = "https://claude.ai/login?client_id=ml-agent&redirect_uri=http://localhost:8888/callback&scope=profile%20email"

    # Start OAuth flow
    auth_code = oauth_login_flow("Claude Pro", oauth_url)

    if not auth_code:
        print("❌ Authentication failed")
        return False

    # Save credentials
    oauth_manager.authenticate_claude_oauth(auth_code)

    print("✓ Claude Pro login successful!")
    print(f"✓ Token saved to ~/.ml-agent/auth.json")

    return True


def login_openai():
    """Login to ChatGPT Plus via OAuth."""
    oauth_manager = OAuthManager()

    # OAuth URL (in real app, would be from OpenAI)
    oauth_url = "https://auth.openai.com/authorize?client_id=ml-agent&redirect_uri=http://localhost:8888/callback&scope=openai.profile%20openai.email&response_type=code"

    # Start OAuth flow
    auth_code = oauth_login_flow("ChatGPT Plus", oauth_url)

    if not auth_code:
        print("❌ Authentication failed")
        return False

    # Save credentials
    oauth_manager.authenticate_openai_oauth(auth_code)

    print("✓ ChatGPT Plus login successful!")
    print(f"✓ Token saved to ~/.ml-agent/auth.json")

    return True


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 login.py [claude|openai|status]\n")
        print("Examples:")
        print("  python3 login.py claude    # Login to Claude Pro")
        print("  python3 login.py openai    # Login to ChatGPT Plus")
        print("  python3 login.py status    # Show status")
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "status":
        show_status()

    elif command == "claude":
        success = login_claude()
        sys.exit(0 if success else 1)

    elif command == "openai":
        success = login_openai()
        sys.exit(0 if success else 1)

    else:
        print(f"❌ Unknown command: {command}")
        sys.exit(1)
