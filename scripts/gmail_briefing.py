#!/usr/bin/env python3
"""Search school mail and send the weekly HTML briefing via the Gmail API.

Used by Sunday cloud automations when Cursor does not register the Gmail MCP
server. Credentials come from environment secrets only — never from the repo.

  GMAIL_CLIENT_ID
  GMAIL_CLIENT_SECRET
  GMAIL_REFRESH_TOKEN

One-time local setup: python3 scripts/gmail_oauth_setup.py
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_HTML = ROOT / "email" / "weekly-briefing.html"
DEFAULT_ASSETS = ROOT / "email" / "assets"
DEFAULT_TO = "kotolynski@gmail.com"
AVATAR_FILES = ("avatar-eldor.png", "avatar-malte.png", "avatar-vega-lo.png")

SEARCH_QUERIES = [
    "from:tokyois.com newer_than:14d in:anywhere",
    "from:openapply.com newer_than:14d in:anywhere",
    "(from:toddleapp.com OR from:toddle) newer_than:14d in:anywhere",
    "(from:managebac.com OR from:managebac) newer_than:14d in:anywhere",
    "from:schoolsbuddy newer_than:14d in:anywhere",
    "from:seesaw newer_than:14d in:anywhere",
    '("Tokyo International School" OR TIS OR tokyois) newer_than:14d in:anywhere',
]

TOKEN_URL = "https://oauth2.googleapis.com/token"
GMAIL_API = "https://gmail.googleapis.com/gmail/v1/users/me"


def _require_secrets() -> tuple[str, str, str]:
    missing = [
        name
        for name in ("GMAIL_CLIENT_ID", "GMAIL_CLIENT_SECRET", "GMAIL_REFRESH_TOKEN")
        if not os.environ.get(name, "").strip()
    ]
    if missing:
        sys.exit(
            "Missing secrets: "
            + ", ".join(missing)
            + ". Add them as Cursor Cloud / automation secrets, then re-run. "
            "Create the refresh token once with: python3 scripts/gmail_oauth_setup.py"
        )
    return (
        os.environ["GMAIL_CLIENT_ID"].strip(),
        os.environ["GMAIL_CLIENT_SECRET"].strip(),
        os.environ["GMAIL_REFRESH_TOKEN"].strip(),
    )


def access_token() -> str:
    client_id, client_secret, refresh = _require_secrets()
    body = urllib.parse.urlencode(
        {
            "client_id": client_id,
            "client_secret": client_secret,
            "refresh_token": refresh,
            "grant_type": "refresh_token",
        }
    ).encode()
    req = urllib.request.Request(
        TOKEN_URL,
        data=body,
        method="POST",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            payload = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        sys.exit(f"OAuth token refresh failed ({exc.code}). Re-run gmail_oauth_setup.py.")
    token = payload.get("access_token")
    if not token:
        sys.exit("OAuth token refresh returned no access_token.")
    return token


def _gmail(token: str, method: str, path: str, data: dict | None = None) -> dict:
    url = f"{GMAIL_API}{path}"
    raw = None if data is None else json.dumps(data).encode()
    req = urllib.request.Request(
        url,
        data=raw,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            **({"Content-Type": "application/json"} if raw else {}),
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            return json.loads(resp.read().decode() or "{}")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:500]
        sys.exit(f"Gmail API {method} {path} failed ({exc.code}): {detail}")


def rewrite_html_cids(html: str) -> str:
    """In-memory only. On-disk template keeps relative assets/ paths."""
    return re.sub(
        r'(src=["\'])assets/(avatar-(?:eldor|malte|vega-lo)\.png)(["\'])',
        r"\1cid:\2\3",
        html,
    )


def build_mime(
    *,
    to: str,
    subject: str,
    html: str,
    body: str,
    asset_dir: Path,
    from_addr: str | None = None,
) -> bytes:
    html_cid = rewrite_html_cids(html)
    related = MIMEMultipart("related")
    related["To"] = to
    related["Subject"] = subject
    related["Date"] = formatdate(localtime=True)
    if from_addr:
        related["From"] = from_addr

    alternative = MIMEMultipart("alternative")
    alternative.attach(MIMEText(body, "plain", "utf-8"))
    alternative.attach(MIMEText(html_cid, "html", "utf-8"))
    related.attach(alternative)

    for name in AVATAR_FILES:
        path = asset_dir / name
        if not path.is_file():
            sys.exit(f"Missing inline avatar: {path}")
        image = MIMEImage(path.read_bytes(), _subtype="png", name=name)
        image.add_header("Content-ID", f"<{name}>")
        image.add_header("Content-Disposition", "inline", filename=name)
        related.attach(image)
    return related.as_bytes()


def cmd_check(_: argparse.Namespace) -> None:
    _require_secrets()
    print("gmail secrets present")


def cmd_search(_: argparse.Namespace) -> None:
    token = access_token()
    seen: dict[str, dict] = {}
    for query in SEARCH_QUERIES:
        listed = _gmail(
            token,
            "GET",
            "/messages?" + urllib.parse.urlencode({"q": query, "maxResults": 50}),
        )
        for item in listed.get("messages") or []:
            msg_id = item["id"]
            if msg_id in seen:
                continue
            meta = _gmail(
                token,
                "GET",
                f"/messages/{urllib.parse.quote(msg_id)}"
                + "?"
                + urllib.parse.urlencode(
                    [
                        ("format", "metadata"),
                        ("metadataHeaders", "From"),
                        ("metadataHeaders", "Subject"),
                        ("metadataHeaders", "Date"),
                    ]
                ),
            )
            headers = {
                h["name"].lower(): h.get("value", "")
                for h in (meta.get("payload") or {}).get("headers") or []
            }
            seen[msg_id] = {
                "id": msg_id,
                "threadId": item.get("threadId"),
                "from": headers.get("from", ""),
                "subject": headers.get("subject", ""),
                "date": headers.get("date", ""),
                "snippet": meta.get("snippet", ""),
                "query": query,
            }
    print(json.dumps({"count": len(seen), "messages": list(seen.values())}, indent=2))


def cmd_read(args: argparse.Namespace) -> None:
    token = access_token()
    msg = _gmail(
        token,
        "GET",
        f"/messages/{urllib.parse.quote(args.id)}?format=full",
    )
    print(json.dumps(msg, indent=2)[:20000])


def cmd_send(args: argparse.Namespace) -> None:
    html_path = Path(args.html)
    if not html_path.is_file():
        sys.exit(f"HTML template not found: {html_path}")
    html = html_path.read_text(encoding="utf-8")
    if "<!DOCTYPE html" not in html[:200] and "<html" not in html[:400].lower():
        sys.exit("Refusing to send: html file is not a full HTML document.")
    mime = build_mime(
        to=args.to,
        subject=args.subject,
        html=html,
        body=args.body,
        asset_dir=Path(args.assets),
    )
    if args.dry_run:
        out = Path(args.dry_run)
        out.write_bytes(mime)
        print(f"wrote MIME to {out} (not sent)")
        return
    token = access_token()
    profile = _gmail(token, "GET", "/profile")
    raw = base64.urlsafe_b64encode(mime).decode().rstrip("=")
    result = _gmail(token, "POST", "/messages/send", {"raw": raw})
    print(
        json.dumps(
            {
                "sent": True,
                "id": result.get("id"),
                "threadId": result.get("threadId"),
                "from": profile.get("emailAddress"),
                "to": args.to,
                "subject": args.subject,
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    sub.add_parser("check", help="Verify Gmail secrets exist (does not print them)")
    sub.add_parser("search", help="Search school mail from the last 14 days")

    read_p = sub.add_parser("read", help="Read one message by Gmail id")
    read_p.add_argument("id")

    send_p = sub.add_parser("send", help="Send the filled weekly-briefing HTML")
    send_p.add_argument("--to", default=DEFAULT_TO)
    send_p.add_argument("--subject", required=True)
    send_p.add_argument("--html", default=str(DEFAULT_HTML))
    send_p.add_argument("--body", required=True, help="Plain-text fallback, 3–5 sentences")
    send_p.add_argument("--assets", default=str(DEFAULT_ASSETS))
    send_p.add_argument(
        "--dry-run",
        metavar="PATH",
        help="Write the MIME message to PATH instead of sending",
    )

    args = parser.parse_args()
    {"check": cmd_check, "search": cmd_search, "read": cmd_read, "send": cmd_send}[args.cmd](args)


if __name__ == "__main__":
    main()
