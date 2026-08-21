# TIS Weekly Briefing — Architecture

How the system is built.

## Components

```
~/Projects/TIS-Summary/           ← project root (git repo)
├── AGENTS.md                     # Cloud-run instructions: fill template + send HTML
├── memory.md                     # Permanent family/school knowledge (read first)
├── architecture.md               # This file
├── decisions.md                  # Decision log
├── todo.md                       # Next steps
├── TIS-Summary-print.html        # Legacy print/PDF sheet (superseded by email/)
├── email/
│   ├── weekly-briefing.html      # HTML email briefing — MD3, table-based, text-first
│   └── assets/                   # Per-child avatars (the email's only images)
│       ├── avatar-eldor.png      # 128px, circular mask + white ring baked in
│       ├── avatar-malte.png
│       └── avatar-vega-lo.png
└── scripts/
    ├── resend_briefing.py        # Preferred cloud send: Resend API + one secret
    ├── gmail_briefing.py         # Gmail API search + HTML send (optional fallback)
    └── gmail_oauth_setup.py      # One-time local Gmail refresh-token helper

~/.cursor/skills/tis-weekly-briefing/
└── SKILL.md                      # Agent instructions (primary entry point)

~/.cursor/commands/
└── tis-week.md                   # Slash command definition → triggers the skill

~/.cursor/projects/TIS-Summary/canvases/
└── TIS-Summary.canvas.tsx        # Overwritten each run with the weekly briefing
```

## Data flow (each run)

1. Agent reads `memory.md` and `AGENTS.md`.
2. Agent searches Gmail via Gmail MCP when registered; otherwise `python3 scripts/gmail_briefing.py search` using Cloud secrets.
3. Agent logs into portal.tokyois.com when a browser is available; otherwise Gmail-only.
4. Agent deduplicates 3-child mail, extracts events + actions for the coming week.
5. Agent overwrites `email/weekly-briefing.html` with this week's data (same MD3 table layout).
6. Agent overwrites `TIS-Summary.canvas.tsx` when a canvas workspace is available.
7. On Sunday (or when asked to send): Gmail MCP `send_message` if available, else `scripts/resend_briefing.py send`, else `scripts/gmail_briefing.py send`. HTML plus inline avatar CIDs. A short chat recap is the run log, not the email.

## Trigger paths

| How | What happens |
|---|---|
| `/tis-week` in chat | Runs the skill on demand |
| Sunday automation | Cloud agent clones this repo, fills the HTML template, sends via Resend (preferred) or Gmail MCP/API |

The Sunday prompt must say **fill and send `email/weekly-briefing.html`**. If it only says "send a summary", the agent emails its chat recap as plain text — that is what happened on 20 Aug 2026.

## MCP dependencies

| MCP | Used for | Status |
|---|---|---|
| `gmail` (Cursor Gmail plugin) | Search + send | **Desktop chat: works.** Cloud Sunday automation: plugin files sync as static; no `gmail` MCP server is registered. |
| Resend API (`scripts/resend_briefing.py`) | Send HTML briefing | **Preferred cloud send.** Secret `RESEND_API_KEY` (optional `RESEND_FROM`). Does not search Gmail. |
| Gmail API (`scripts/gmail_briefing.py`) | Search + send when MCP is missing | Optional. Secrets `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`. |
| `cursor-ide-browser` | portal.tokyois.com login + scraping | Desktop only. Cloud runs: Gmail-only is the contract; portal can still be fetched with HTTP login (skip honeypot `um_request`). |
| `cursor-app-control` | Open Automations editor | Desktop only |

If Gmail MCP, `RESEND_API_KEY`, and the Gmail API secrets are all missing, **do not send**. Never substitute a markdown recap.

## Resend (preferred cloud send)

One Cursor secret. No Google OAuth.

1. Create an API key at https://resend.com/api-keys
2. Add `RESEND_API_KEY` as a **Runtime Secret** at https://cursor.com/dashboard/cloud-agents
3. Optional: verify a domain at https://resend.com/domains and set `RESEND_FROM` to `TIS Week <you@that-domain>`. Until then the script uses Resend’s onboarding sender `beth.t@example.com` (fine for sending to `kotolynski@gmail.com` while testing).
4. Start a **new** cloud/automation run. This VM does not pick up secrets after boot.
5. Resend POSTs must send `User-Agent: TIS-Summary-resend/1.0`. Cloudflare returns 1010 if the default Python UA is used.

## Gmail API secrets (optional search + send)

One-time, on Fredrik’s laptop (needs a browser):

1. [Google Cloud Console](https://console.cloud.google.com/) → project → enable **Gmail API**.
2. OAuth consent screen (External) → add `kotolynski@gmail.com` as a test user.
3. Credentials → Create OAuth client ID → **Desktop app**. Copy client id and secret.
4. `python3 scripts/gmail_oauth_setup.py --client-id … --client-secret …`
5. Paste the three printed values as Cursor Cloud / environment secrets (not into git):
   - `GMAIL_CLIENT_ID`
   - `GMAIL_CLIENT_SECRET`
   - `GMAIL_REFRESH_TOKEN`

Redirect URI used by the helper: `http://127.0.0.1:8765/oauth2callback`. Add it on the OAuth client if Google asks.

Scopes: `gmail.readonly` and `gmail.send`. The next Sunday run can then search and send without Gmail MCP.

## Output artifacts

There are two renderings of the same briefing data. Both are overwritten each run.

### 1. Canvas — `~/.cursor/projects/TIS-Summary/canvases/TIS-Summary.canvas.tsx`

For reading beside chat. Uses `cursor/canvas` SDK only (no external imports, no fetch, all data inline). Sections: urgent actions → stats → week-at-a-glance table → Monday detail → per-child cards → daily operations → upcoming → contacts → sources.

### 2. HTML email — `email/weekly-briefing.html`

For sending, forwarding to a partner, or printing to PDF. Self-contained single file, no external assets.

Section order (fixed): hero → urgent actions → this week's highlights → week timeline → per child → upcoming events → helpful links → footer.

Email-client constraints that shape the markup:

| Constraint | Consequence |
|---|---|
| Outlook uses the Word engine | Layout is `<table role="presentation">` only. No flexbox, no grid. |
| Gmail strips `<style>` in some contexts | All visual styling is inline. `<style>` holds only resets and media queries. |
| Outlook ignores `border-radius` / `box-shadow` | Cards degrade to square. We do **not** add a gray `border` as compensation — Fredrik asked borders off. Colour and padding still separate the cards. |
| Outlook ignores media queries | The 640px desktop layout is the fallback and is correct there. |
| Remote images are blocked by default | Everything except the three per-child avatars is live HTML text. Each avatar has the child's name as alt text, so a blocked image degrades to the name. |
| Outlook ignores `border-radius` on images | The circle and white ring are baked into each avatar PNG with transparent corners, so avatars stay round everywhere. |
| Relative image paths do not resolve in mail clients | At send time, rewrite avatar `src` to `cid:<filename>` and attach the three PNGs as inline Gmail attachments. The on-disk template keeps relative `assets/` paths for local preview. |
| No JavaScript | The Print/PDF button is browser-only; it is inert in mail clients. |

Equal-height paired cards are achieved by making the `<td>` itself the card (background, radius, padding) rather than nesting a table inside it — cells in a table row are equal height by definition, whereas `height:100%` on a nested table does not resolve against an auto-height cell. Those cells therefore need `box-sizing:border-box` when they go full-width at the mobile breakpoint.

Responsive breakpoint: 620px. Verified with no horizontal overflow at 375px and 414px.
