"""
OAuth Server for Local Authentication
Handles OAuth flow with callback server.
"""

import json
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import threading
from typing import Optional


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """Handle OAuth callback requests."""

    auth_code = None

    def do_GET(self):
        """Handle GET request from OAuth callback."""
        parsed_url = urlparse(self.path)
        query_params = parse_qs(parsed_url.query)

        if "code" in query_params:
            OAuthCallbackHandler.auth_code = query_params["code"][0]

            # Send success response
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = """
            <html>
            <head><title>Authentication Successful</title></head>
            <body>
                <h1>✓ Authentication Successful!</h1>
                <p>You can close this window and return to the terminal.</p>
                <p>Your auth code has been captured.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
        else:
            # Send error response
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()

            html = """
            <html>
            <head><title>Authentication Failed</title></head>
            <body>
                <h1>✗ Authentication Failed</h1>
                <p>No auth code received.</p>
            </body>
            </html>
            """
            self.wfile.write(html.encode())

    def log_message(self, format, *args):
        """Suppress log messages."""
        pass


class OAuthServer:
    """Local OAuth server for authentication flow."""

    def __init__(self, port: int = 8888):
        self.port = port
        self.server: Optional[HTTPServer] = None
        self.auth_code: Optional[str] = None

    def start(self) -> None:
        """Start OAuth callback server."""
        self.server = HTTPServer(("localhost", self.port), OAuthCallbackHandler)

        # Run server in background thread
        server_thread = threading.Thread(target=self.server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

    def stop(self) -> None:
        """Stop OAuth server."""
        if self.server:
            self.server.shutdown()

    def get_auth_code(self) -> Optional[str]:
        """Get captured auth code."""
        return OAuthCallbackHandler.auth_code

    def open_browser(self, oauth_url: str) -> None:
        """Open browser to OAuth URL."""
        webbrowser.open(oauth_url)

    def wait_for_callback(self, timeout: int = 300) -> Optional[str]:
        """Wait for OAuth callback."""
        import time

        start = time.time()
        while time.time() - start < timeout:
            auth_code = self.get_auth_code()
            if auth_code:
                return auth_code
            time.sleep(0.5)

        return None


def oauth_login_flow(provider: str, oauth_url: str) -> Optional[str]:
    """Execute OAuth login flow."""
    print(f"\n🔐 Starting OAuth flow for {provider}...\n")

    # Start local callback server
    server = OAuthServer(port=8888)
    server.start()

    print(f"Opening browser to authenticate...")
    print(f"URL: {oauth_url}\n")

    # Open browser
    server.open_browser(oauth_url)

    print("Waiting for authentication...")
    print("(This will timeout in 5 minutes)\n")

    # Wait for callback
    auth_code = server.wait_for_callback(timeout=300)

    server.stop()

    if auth_code:
        print(f"\n✓ Authentication successful!")
        print(f"Auth code: {auth_code[:20]}...\n")
        return auth_code
    else:
        print(f"\n✗ Authentication timeout or failed\n")
        return None
