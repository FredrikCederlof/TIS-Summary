# TIS Weekly Briefing — Todo

Next steps. Move done items to decisions.md or delete them.

## Open

- [ ] **Add Gmail API Cloud secrets** (optional) — only if inbox search from cloud is needed. `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`.
- [ ] **Decide whether the email replaces `TIS-Summary-print.html`** — `email/weekly-briefing.html` now covers the same content and also prints cleanly. The old print sheet uses CSS Grid/Flexbox and is not email-safe. Delete it once confirmed.
- [ ] **Verify bus situation** — Bus requests were removed from re-enrolment (March 2026). Confirm if bus is still needed for any child.
- [ ] **Update memory.md with House Team colours** — Sheet published 16 Sep; colours not extracted (needs login).
- [ ] **Finish conference bookings** — sign-up closes Tue 3 Nov 21:00. Slots already booked for all three; add/cancel extra US teachers if needed.
- [ ] **Rank Eldor Season 2 CCA** — SchoolsBuddy by Tue 3 Nov 15:00.
- [ ] **Rank Malte and Vega-Lo Season 2 CCA** — opens Tue 3 Nov 15:00, closes Mon 9 Nov 15:00.
- [ ] **Eldor Japanese homework** — due Tue 3 Nov (Chika / Toddle).
- [ ] **G3 Amazon Chiba volunteers** — 3 Dec; email Jared/Sarah if a parent can go.

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
- [x] Book Lower School / November conferences — SchoolsBuddy confirmation 25 Oct for all three
- [x] Pay TFC Halloween tickets / party Fri 30 Oct
- [x] Sunday 1 Nov 2026 briefing filled for 2–8 Nov and sent via Resend (`01a19695-7fae-703b-a012-e970dccaf986`)
