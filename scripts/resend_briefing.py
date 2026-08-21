#!/usr/bin/env python3
"""Send the weekly HTML briefing via Resend.

Preferred cloud send path: one Cursor secret, no Google OAuth.

  RESEND_API_KEY     required
  RESEND_FROM        optional, default TIS Week <beth.t@example.com>
                     (Resend onboarding address). After you verify a domain,
                     set e.g. TIS Week <briefing@insightworks.se>

Does not search Gmail. Portal + memory still fill the template.
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


def _dedupe(addrs: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for raw in addrs:
        addr = (raw or "").strip()
        if not addr:
            continue
        key = addr.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(addr)
    return out


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
        "to": _dedupe(to),
        "subject": subject,
        "html": rewrite_html_cids(html),
        "text": body,
        "attachments": attachments,
    }
    cc_list = _dedupe(cc)
    if cc_list:
        payload["cc"] = cc_list
    if not payload["to"]:
        sys.exit("Refusing to send: no --to recipients.")
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
    payload = build_payload(
        to=args.to or [DEFAULT_TO],
        cc=args.cc or [],
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
            "User-Agent": "TIS-Summary-resend/1.0",
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
            {
                "sent": True,
                **result,
                "to": payload["to"],
                "cc": payload.get("cc", []),
                "subject": args.subject,
            },
            indent=2,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check", help="Verify RESEND_API_KEY exists")
    send_p = sub.add_parser("send", help="Send the filled weekly-briefing HTML")
    send_p.add_argument(
        "--to",
        action="append",
        help="Recipient. Repeatable. Defaults to kotolynski@gmail.com.",
    )
    send_p.add_argument(
        "--cc",
        action="append",
        help="CC recipient. Repeatable. Always include sternersofia@gmail.com on Sunday.",
    )
    send_p.add_argument("--subject", required=True)
    send_p.add_argument("--html", default=str(DEFAULT_HTML))
    send_p.add_argument("--body", required=True)
    send_p.add_argument("--assets", default=str(DEFAULT_ASSETS))
    send_p.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    {"check": cmd_check, "send": cmd_send}[args.cmd](args)


if __name__ == "__main__":
    main()
