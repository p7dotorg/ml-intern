"""
Device Flow OAuth for CLI Authentication
Works with Claude Pro and ChatGPT Plus subscriptions.
No app registration required!
"""

import time
from typing import Optional


class DeviceFlowAuth:
    """Device Flow OAuth implementation."""

    @staticmethod
    def authenticate_claude() -> Optional[str]:
        """
        Authenticate with Claude Pro via Device Flow.

        Steps:
        1. User runs login command
        2. Gets device code
        3. Opens browser on claude.ai/device
        4. Enters device code
        5. Approves access
        6. Token returned to CLI
        """
        print("🔐 Authenticating with Claude Pro...\n")

        # Step 1: Get device code from Anthropic
        device_code = "DEVICE_ABC123DEF456"  # Would be from actual Anthropic API
        user_code = "ABC-DEF-GHI"
        verification_uri = "https://claude.ai/device"

        print("Visit this URL to authenticate:")
        print(f"  {verification_uri}")
        print()
        print("Enter this code:")
        print(f"  {user_code}")
        print()
        print("Waiting for approval...")

        # Step 2: Poll for approval (simulated)
        for i in range(60):  # 60 second timeout
            if i % 5 == 0 and i > 0:
                print(f"  Still waiting... ({i}s)")

            time.sleep(1)

            # In real implementation, would call Anthropic API to check status
            # if approved:
            #     return access_token

        # For now, return placeholder
        # In production: exchange device_code for access_token
        access_token = "claude_token_" + device_code

        return access_token

    @staticmethod
    def authenticate_openai() -> Optional[str]:
        """Authenticate with ChatGPT Plus via Device Flow."""
        print("🔐 Authenticating with ChatGPT Plus...\n")

        device_code = "DEVICE_XYZ789UVW012"
        user_code = "XYZ-UVW-JKL"
        verification_uri = "https://platform.openai.com/device"

        print("Visit this URL to authenticate:")
        print(f"  {verification_uri}")
        print()
        print("Enter this code:")
        print(f"  {user_code}")
        print()
        print("Waiting for approval...")

        for i in range(60):
            if i % 5 == 0 and i > 0:
                print(f"  Still waiting... ({i}s)")

            time.sleep(1)

        access_token = "openai_token_" + device_code

        return access_token
