# TIS Weekly Briefing — Todo

Next steps. Move done items to decisions.md or delete them.

## Open

- [ ] **Add Gmail API Cloud secrets** (optional) — only if inbox search from cloud is needed. `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`.
- [ ] **Decide whether the email replaces `TIS-Summary-print.html`** — `email/weekly-briefing.html` now covers the same content and also prints cleanly. The old print sheet uses CSS Grid/Flexbox and is not email-safe. Delete it once confirmed.
- [ ] **Verify bus situation** — Bus requests were removed from re-enrolment (March 2026). Confirm if bus is still needed for any child.
- [ ] **Update memory.md with House Team colours** — Sheet published 16 Sep; colours not extracted (needs login).
- [ ] **Book Lower School conferences** — SchoolsBuddy Mon 26 Oct–Tue 3 Nov for Malte and Vega-Lo.
- [ ] **Pay TFC Halloween tickets** — if RSVP’d; due Wed 28 Oct. Party Fri 30 Oct 17:15 Gym 1F.
- [ ] **Season 2 CCA sign-up** — watch Toddle/SchoolsBuddy after Fall Break; Season 1 ends Fri 13 Nov.

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
- [x] Confirm Eldor's and Malte's class placements — Toddle 21 Aug: 6B / 3B / KA
- [x] Update memory.md with class teachers — Chrissy Erwin; Jared Barnes + Sarah; Claudia Ackermann + Laura
- [x] SchoolsBuddy CCA allocation result — soccer / basketball / Tinker Lab
- [x] Kiwi Kitchen account — in use; skip Vega-Lo lunch Wed 28 Oct (Asobono picnic)
- [x] Sunday 25 Oct 2026 briefing filled for 26 Oct–1 Nov and sent via Resend
