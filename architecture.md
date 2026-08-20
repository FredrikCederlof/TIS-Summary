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
└── email/
    ├── weekly-briefing.html      # HTML email briefing — MD3, table-based, text-first
    └── assets/                   # Per-child avatars (the email's only images)
        ├── avatar-eldor.png      # 128px, circular mask + white ring baked in
        ├── avatar-malte.png
        └── avatar-vega-lo.png

~/.cursor/skills/tis-weekly-briefing/
└── SKILL.md                      # Agent instructions (primary entry point)

~/.cursor/commands/
└── tis-week.md                   # Slash command definition → triggers the skill

~/.cursor/projects/TIS-Summary/canvases/
└── TIS-Summary.canvas.tsx        # Overwritten each run with the weekly briefing
```

## Data flow (each run)

1. Agent reads `memory.md` and `AGENTS.md`.
2. Agent searches Gmail via Gmail MCP (multiple queries, see AGENTS.md / SKILL.md).
3. Agent logs into portal.tokyois.com when a browser is available; otherwise Gmail-only.
4. Agent deduplicates 3-child mail, extracts events + actions for the coming week.
5. Agent overwrites `email/weekly-briefing.html` with this week's data (same MD3 table layout).
6. Agent overwrites `TIS-Summary.canvas.tsx` when a canvas workspace is available.
7. On Sunday (or when asked to send): Gmail `send_message` with `htmlBody` = the filled HTML, plus inline avatar attachments. A short chat recap is the run log, not the email.

## Trigger paths

| How | What happens |
|---|---|
| `/tis-week` in chat | Runs the skill on demand |
| Sunday automation | Cloud agent clones this repo, fills the HTML template, sends it via Gmail MCP |

The Sunday prompt must say **fill and send `email/weekly-briefing.html`**. If it only says "send a summary", the agent emails its chat recap as plain text — that is what happened on 20 Aug 2026.

## MCP dependencies

| MCP | Used for | Status |
|---|---|---|
| `gmail` (Cursor Gmail plugin → `https://gmailmcp.googleapis.com/mcp/v1`) | Search school mail + `send_message` with HTML | **Desktop: connected. Cloud Sunday automation: not registered.** Plugin files land in `~/.cursor/plugins/cache`, but `GetMcpTools` does not expose a `gmail` server (OAuth does not attach). 20 Aug 2026 run failed send for this reason. |
| `cursor-ide-browser` | portal.tokyois.com login + scraping | Desktop only. Cloud runs: Gmail-only is the contract; portal can still be fetched with HTTP login (skip honeypot `um_request`). |
| `cursor-app-control` | Open Automations editor | Desktop only |

If Gmail MCP is missing, **do not send**. Report the failure in the run log. Never substitute a markdown recap.

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
