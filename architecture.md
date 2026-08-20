# TIS Weekly Briefing — Architecture

How the system is built.

## Components

```
~/Projects/TIS-Summary/           ← project root (git repo)
├── memory.md                     # Permanent family/school knowledge (read first)
├── architecture.md               # This file
├── decisions.md                  # Decision log
└── todo.md                       # Next steps

~/.cursor/skills/tis-weekly-briefing/
└── SKILL.md                      # Agent instructions (primary entry point)

~/.cursor/commands/
└── tis-week.md                   # Slash command definition → triggers the skill

~/.cursor/projects/TIS-Summary/canvases/
└── TIS-Summary.canvas.tsx        # Overwritten each run with the weekly briefing
```

## Data flow (each run)

1. Agent reads `memory.md` → has family/school context without searching history.
2. Agent searches Gmail via Gmail MCP (multiple queries, see SKILL.md).
3. Agent logs into portal.tokyois.com (credentials in memory.md) to collect TIS Times, calendar, notices.
4. Agent deduplicates 3-child mail, extracts events + actions for the coming week.
5. Agent overwrites `TIS-Summary.canvas.tsx` with the structured briefing.
6. Agent posts a short chat recap of actions that cannot wait.

## Trigger paths

| How | What happens |
|---|---|
| `/tis-week` in chat | Runs the skill on demand |
| Sunday 19:00 automation | Cursor Automation (cron `0 19 * * 0`) — draft approved, not yet saved |

## MCP dependencies

| MCP | Used for | Status |
|---|---|---|
| `gmail` (plugin-gmail-gmail) | Search + read school mail | Connected |
| `cursor-ide-browser` | portal.tokyois.com login + scraping | Connected (shared session) |
| `cursor-app-control` | Open Automations editor | Connected |

## Canvas

File: `~/.cursor/projects/TIS-Summary/canvases/TIS-Summary.canvas.tsx`

Overwritten on every run. Uses `cursor/canvas` SDK only (no external imports, no fetch, all data inline). Sections: urgent actions → stats → week-at-a-glance table → Monday detail → per-child cards → daily operations → upcoming → contacts → sources.
