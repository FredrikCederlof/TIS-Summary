# TIS Weekly Briefing — Todo

Next steps. Move done items to decisions.md or delete them.

## Open

- [ ] **Add Gmail API Cloud secrets** (optional) — only if inbox search from cloud is needed. `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`.
- [ ] **Decide whether the email replaces `TIS-Summary-print.html`** — `email/weekly-briefing.html` now covers the same content and also prints cleanly. The old print sheet uses CSS Grid/Flexbox and is not email-safe. Delete it once confirmed.
- [ ] **Verify bus situation** — Bus requests were removed from re-enrolment (March 2026). Confirm if bus is still needed for any child.
- [ ] **Update memory.md with House Team colours** — Assigned in first full week of school (week of 25 Aug). Still unknown as of 13 Sep.
- [ ] **Eldor Japanese placement** — Review window was late Aug / week of 7 Sep. No final mail by 13 Sep. Watch Toddle.
- [ ] **Eldor JUMP trip 13–16 Oct** — G6–8. Watch Toddle for kit / consent once issued.
- [ ] **Merge Sunday briefing PRs** — weekly HTML updates sit on draft automation branches; main still has the 24–30 Aug template.

## Done

- [x] Gmail MCP connected and tested (Aug 2026)
- [x] Skill created at `~/.cursor/skills/tis-weekly-briefing/SKILL.md`
- [x] Command `/tis-week` created at `~/.cursor/commands/tis-week.md`
- [x] Canvas `TIS-Summary.canvas.tsx` created and validated (no TS errors)
- [x] Knowledge files created: memory.md, architecture.md, decisions.md, todo.md
- [x] First full briefing run: week of 24–30 Aug 2026
- [x] MD3 HTML email built at `email/weekly-briefing.html` — table-based, responsive, verified at 320/375/414/640px
- [x] UX review checklist applied across all eight sections (20 Aug 2026)
- [x] Per-child avatars added, replacing the letter monograms
- [x] Skill + AGENTS.md require sending the filled HTML via Gmail `htmlBody` (20 Aug 2026)
- [x] `email/` + `AGENTS.md` are on origin/main (Sunday cloud clone had the template)
- [x] Sunday automation prompt now names the HTML template (20 Aug 2026) — send still blocked until Gmail MCP attaches in cloud
- [x] Gmail API fallback scripts (`scripts/gmail_briefing.py`, `gmail_oauth_setup.py`) (20 Aug 2026)
- [x] Resend send script (`scripts/resend_briefing.py`) as preferred cloud path (20 Aug 2026)
- [x] Resend Cloud secrets injected (`RESEND_API_KEY`, `RESEND_FROM`) — Sunday sends from 21 Aug through 6 Sep succeeded
- [x] Class placements confirmed (Toddle 21 Aug): Eldor 6B / Malte 3B / Vega-Lo KA
- [x] Class teachers recorded: Chrissy Erwin; Jared Barnes + Sarah; Claudia Ackermann + Laura
- [x] CCA Season 1 allocations recorded (SchoolsBuddy 28 Aug)
- [x] Sunday 13 Sep briefing filled for 14–20 Sep from Gmail
