#!/usr/bin/env python3
"""Send the weekly HTML briefing via Resend.

Preferred cloud send path: one Cursor secret, no Google OAuth.

  RESEND_API_KEY     required
  RESEND_FROM        optional, default TIS Week <beth.t@example.com>
                     (Resend onboarding address). After you verify a domain,
                     set e.g. TIS Week <briefing@insightworks.se>

Does not search Gmail. Portal + memory still fill the template.

Accepts repeated --to / --cc. POSTs send User-Agent so Cloudflare does not
block the request (1010).
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from gmail_briefing import (  # noqa: E402
    AVATAR_FILES,
    DEFAULT_ASSETS,
    DEFAULT_HTML,
    DEFAULT_TO,
    rewrite_html_cids,
)

RESEND_URL = "https://api.resend.com/emails"
DEFAULT_FROM = "TIS Week <beth.t@example.com>"
USER_AGENT = "TIS-Summary-resend/1.0"


def _api_key() -> str:
    key = os.environ.get("RESEND_API_KEY", "").strip()
    if not key:
        sys.exit(
            "Missing secret RESEND_API_KEY. Create a key at https://resend.com/api-keys "
            "and add it as a Cursor Cloud Runtime Secret, then start a new run."
        )
    return key


def _from_addr() -> str:
    return os.environ.get("RESEND_FROM", "").strip() or DEFAULT_FROM


def _unique_addrs(values: list[str] | None, fallback: str | None = None) -> list[str]:
    seen: list[str] = []
    for raw in values or []:
        addr = (raw or "").strip()
        if addr and addr not in seen:
            seen.append(addr)
    if not seen and fallback:
        seen.append(fallback)
    return seen


def build_payload(
    *,
    to: list[str],
    cc: list[str],
    subject: str,
    html: str,
    body: str,
    asset_dir: Path,
) -> dict:
    attachments = []
    for name in AVATAR_FILES:
        path = asset_dir / name
        if not path.is_file():
            sys.exit(f"Missing inline avatar: {path}")
        attachments.append(
            {
                "filename": name,
                "content": base64.b64encode(path.read_bytes()).decode(),
                "content_id": name,
            }
        )
    payload = {
        "from": _from_addr(),
        "to": to,
        "subject": subject,
        "html": rewrite_html_cids(html),
        "text": body,
        "attachments": attachments,
    }
    if cc:
        payload["cc"] = cc
    return payload


def cmd_check(_: argparse.Namespace) -> None:
    _api_key()
    print(f"RESEND_API_KEY present; from={_from_addr()}")


def cmd_send(args: argparse.Namespace) -> None:
    html_path = Path(args.html)
    if not html_path.is_file():
        sys.exit(f"HTML template not found: {html_path}")
    html = html_path.read_text(encoding="utf-8")
    if "<!DOCTYPE html" not in html[:200] and "<html" not in html[:400].lower():
        sys.exit("Refusing to send: html file is not a full HTML document.")
    to = _unique_addrs(args.to, DEFAULT_TO)
    cc = _unique_addrs(args.cc)
    payload = build_payload(
        to=to,
        cc=cc,
        subject=args.subject,
        html=html,
        body=args.body,
        asset_dir=Path(args.assets),
    )
    if args.dry_run:
        preview = {
            "from": payload["from"],
            "to": payload["to"],
            "cc": payload.get("cc", []),
            "subject": payload["subject"],
            "text": payload["text"],
            "html_has_cid": "cid:avatar-eldor.png" in payload["html"],
            "html_keeps_assets_on_disk": 'src="assets/avatar-eldor.png"'
            in html_path.read_text(encoding="utf-8"),
            "attachments": [a["filename"] for a in payload["attachments"]],
        }
        print(json.dumps(preview, indent=2))
        return

    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        RESEND_URL,
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
            "User-Agent": USER_AGENT,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors="replace")[:800]
        sys.exit(f"Resend send failed ({exc.code}): {detail}")
    print(
        json.dumps(
            {"sent": True, **result, "to": to, "cc": cc, "subject": args.subject},
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="Verify RESEND_API_KEY exists")
    send_p = sub.add_parser("send", help="Send the filled weekly-briefing HTML")
    send_p.add_argument("--to", action="append", default=None)
    send_p.add_argument("--cc", action="append", default=None)
    send_p.add_argument("--subject", required=True)
    send_p.add_argument("--html", default=str(DEFAULT_HTML))
    send_p.add_argument("--body", required=True)
    send_p.add_argument("--assets", default=str(DEFAULT_ASSETS))
    send_p.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    {"check": cmd_check, "send": cmd_send}[args.cmd](args)


if __name__ == "__main__":
    main()
