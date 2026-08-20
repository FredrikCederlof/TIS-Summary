#!/usr/bin/env python3
"""One-time local OAuth for the Sunday Gmail API sender.

Run this on your laptop (needs a browser). It prints a refresh token for
Cursor Cloud secrets. Do not commit the token.

  1. Google Cloud Console → create/select a project
  2. Enable Gmail API
  3. APIs & Services → OAuth consent screen (External, add yourself as test user)
  4. Credentials → Create OAuth client ID → Desktop app
  5. python3 scripts/gmail_oauth_setup.py --client-id ... --client-secret ...

Then add these three secrets to the Cursor environment / automation:

  GMAIL_CLIENT_ID
  GMAIL_CLIENT_SECRET
  GMAIL_REFRESH_TOKEN
"""

from __future__ import annotations

import argparse
import http.server
import json
import threading
import urllib.parse
import urllib.request
import webbrowser

SCOPES = " ".join(
    [
        "https://www.googleapis.com/auth/gmail.readonly",
        "https://www.googleapis.com/auth/gmail.send",
    ]
)
REDIRECT = "http://127.0.0.1:8765/oauth2callback"
AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"


class Handler(http.server.BaseHTTPRequestHandler):
    code: str | None = None
    error: str | None = None

    def do_GET(self) -> None:  # noqa: N802
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/oauth2callback":
            self.send_error(404)
            return
        qs = urllib.parse.parse_qs(parsed.query)
        Handler.error = (qs.get("error") or [None])[0]
        Handler.code = (qs.get("code") or [None])[0]
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(
            b"<html><body><p>You can close this tab and return to the terminal.</p></body></html>"
        )

    def log_message(self, format: str, *args: object) -> None:  # noqa: A003
        return


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client-id", required=True)
    parser.add_argument("--client-secret", required=True)
    args = parser.parse_args()

    params = urllib.parse.urlencode(
        {
            "client_id": args.client_id,
            "redirect_uri": REDIRECT,
            "response_type": "code",
            "scope": SCOPES,
            "access_type": "offline",
            "prompt": "consent",
        }
    )
    server = http.server.HTTPServer(("127.0.0.1", 8765), Handler)
    thread = threading.Thread(target=server.handle_request, daemon=True)
    thread.start()
    url = f"{AUTH_URL}?{params}"
    print("Open this URL if the browser does not launch:\n")
    print(url)
    print()
    webbrowser.open(url)
    thread.join(timeout=180)
    server.server_close()

    if Handler.error:
        raise SystemExit(f"Google OAuth error: {Handler.error}")
    if not Handler.code:
        raise SystemExit("No authorization code. Did the browser redirect to localhost:8765?")

    body = urllib.parse.urlencode(
        {
            "code": Handler.code,
            "client_id": args.client_id,
            "client_secret": args.client_secret,
            "redirect_uri": REDIRECT,
            "grant_type": "authorization_code",
        }
    ).encode()
    req = urllib.request.Request(
        TOKEN_URL,
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.loads(resp.read().decode())
    refresh = payload.get("refresh_token")
    if not refresh:
        raise SystemExit(
            "Google did not return a refresh_token. Re-run with prompt=consent "
            "(this script already sets it) and make sure the OAuth client is a Desktop app."
        )
    print("Add these as Cursor Cloud / automation secrets (do not commit them):\n")
    print(f"GMAIL_CLIENT_ID={args.client_id}")
    print("GMAIL_CLIENT_SECRET=<the secret you passed to this script>")
    print(f"GMAIL_REFRESH_TOKEN={refresh}")


if __name__ == "__main__":
    main()
