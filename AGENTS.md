# TIS weekly briefing — agent instructions

This file is the source of truth for cloud automations. Personal skill `tis-weekly-briefing` mirrors it.

## Goal

Build the coming week's parent briefing from Gmail (and the parent portal when a browser is available), fill the HTML email template, and **send that HTML** to Fredrik. Never send a markdown or plain-text recap as the email.

## Read first

1. `memory.md` — family, children, contacts, credentials
2. `architecture.md` — artifacts and email constraints
3. `todo.md` — open next steps
4. `email/weekly-briefing.html` — the template to fill, not a file to invent from scratch

## Children (always all three)

Per-child order in the email is fixed: **Eldor → Malte → Vega-Lo**.

- Eldor — Grade 6 MYP, returning
- Malte — Grade 3 PYP, returning
- Vega-Lo — Kindergarten, new 2026/27

## Sources

Search Gmail (last 14 days, include trash if school mail was deleted):

```
from:tokyois.com newer_than:14d
from:openapply.com newer_than:14d
from:toddleapp.com OR from:toddle newer_than:14d
from:managebac.com OR from:managebac newer_than:14d
from:schoolsbuddy newer_than:14d
from:seesaw newer_than:14d
("Tokyo International School" OR TIS OR tokyois) newer_than:14d
```

Deduplicate by event + date + action. The same announcement often arrives three times (once per child). Show it once.

If a browser is available, also check https://portal.tokyois.com/ (user `parent` / password `inspire`). Skip the honeypot field (`um_request`). HTTP login without a browser is acceptable: Ultimate Member fields `username-38` / `user_password-38`. If Gmail MCP is missing, say so.

**Preferred cloud send: Resend** (`RESEND_API_KEY`). Skip Google OAuth. Search still uses Gmail MCP/API when available; otherwise portal + memory fill the template.

```
python3 scripts/resend_briefing.py send \
  --to kotolynski@gmail.com \
  --subject "TIS Week · 24–30 Aug 2026" \
  --html email/weekly-briefing.html \
  --body "<3–5 sentence plain-text fallback>"
```

Optional `RESEND_FROM` (default `TIS Week <beth.t@example.com>`). After verifying a domain: `TIS Week <briefing@insightworks.se>`.

**Gmail MCP** still preferred in Cursor Desktop. **Gmail API** (`scripts/gmail_briefing.py`) remains a second fallback if the three Gmail secrets exist.

The scripts rewrite avatar `src` to `cid:` in the payload only. Leave the on-disk template using relative `assets/` paths.

If none of Gmail MCP, `RESEND_API_KEY`, or the Gmail API secrets are available, **do not send**.

## Fill the template

Overwrite `email/weekly-briefing.html` with this week's data.

- Keep the existing Material Design 3 table layout, section order, tokens, and inline styles.
- Do not invent a new layout, markdown email, or "Do this first" bullet list.
- Section order: hero → urgent actions → highlights → week timeline → per child → upcoming events → helpful links → footer.
- Per child: Eldor, then Malte, then Vega-Lo. Cards have no gray border.
- Cards are tonal surfaces (`background-color` + `border-radius`). Do not add `border:1px solid`.
- Preserve all links.

## Send the email (required on Sunday / when asked to send)

Prefer Gmail MCP `send_message` when that server is listed. Otherwise use `scripts/resend_briefing.py send` when `RESEND_API_KEY` is set. Otherwise `scripts/gmail_briefing.py send`. Never send a markdown or chat recap as the email.

| Field | Value |
|---|---|
| to | `kotolynski@gmail.com` |
| subject | `TIS Week · <start>–<end> <Mon>` e.g. `TIS Week · 24–30 Aug 2026` |
| htmlBody | The **full** filled `weekly-briefing.html` document (`<!DOCTYPE html>` through `</html>`) |
| body | 3–5 sentence plain-text fallback covering the hard deadline and first-day facts |

Inline avatars so they survive image blocking:

1. Attach `email/assets/avatar-eldor.png`, `avatar-malte.png`, `avatar-vega-lo.png` as **inline** attachments (`inline: true`, `mimeType: image/png`, filename exactly those names).
2. In `htmlBody` only, rewrite `src="assets/avatar-….png"` to `src="cid:avatar-….png"`. Leave the on-disk template using relative `assets/` paths for local preview.

If the template cannot be filled, **do not send**. Report the failure in the run log instead of falling back to a plain-text briefing.

Chat recap after send: the 3–5 actions that cannot wait. That recap is for the run log, not the email body.

## Cursor Cloud specific instructions

Environment notes for future cloud agents (the startup update script has already run):

- **No dependencies to install.** The scripts in `scripts/` use only the Python 3 standard library (`urllib`, `json`, `base64`, `email`, `http.server`). There is no `requirements.txt`, `venv`, `pyproject.toml`, or lockfile. Just run `python3` (3.12 is present).
- **Nothing to build and no long-running service.** This repo is on-demand CLI scripts plus a static HTML template — there is no dev server, watcher, or daemon to start.
- **No test suite or committed linter.** The `# noqa` comments imply ruff/flake8 was used, but no config is committed. Use `python3 -m py_compile scripts/*.py` as the syntax check.
- **Preview the product** by opening `email/weekly-briefing.html` in a browser; the relative `assets/` avatar paths resolve locally.
- **Exercise the send pipeline without sending** via `python3 scripts/resend_briefing.py send --subject "…" --body "…" --dry-run` (validates the HTML doc, rewrites avatar `src` to `cid:`, and base64-attaches the three avatars).
- **Resend key is send-restricted.** Read endpoints (`GET /domains`, `GET /api-keys`) return `401 restricted_api_key` — that is expected and confirms the key is valid and scoped to send only, not an error.
- **Gmail API fallback needs all three secrets.** In cloud, `GMAIL_REFRESH_TOKEN` is often unset, so `scripts/gmail_briefing.py` search/send will exit with "Missing secrets". Prefer the Gmail MCP (when registered) or Resend; do not treat the missing token as a setup failure.
