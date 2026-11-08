# TIS Weekly Briefing — Todo

Next steps. Move done items to decisions.md or delete them.

## Open

- [ ] **Add Resend Cloud secret** — `RESEND_API_KEY` (Runtime Secret) at https://cursor.com/dashboard/cloud-agents then re-run Sunday. Optional `RESEND_FROM` after domain verify. This is the intended cloud send path.
- [ ] **Add Gmail API Cloud secrets** (optional) — only if inbox search from cloud is needed. `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`.
- [ ] **Decide whether the email replaces `TIS-Summary-print.html`** — `email/weekly-briefing.html` now covers the same content and also prints cleanly. The old print sheet uses CSS Grid/Flexbox and is not email-safe. Delete it once confirmed.
- [ ] **Verify bus situation** — Bus requests were removed from re-enrolment (March 2026). Confirm if bus is still needed for any child.
- [ ] **Update memory.md with House Team colours** — Sheet published 16 Sep; colours not extracted (needs login).
- [ ] **SchoolsBuddy LS Season 2 allocation** — Check Fri 13 Nov for Malte and Vega-Lo. Eldor is KPASS MS Boys Basketball.
- [ ] **G3 Amazon Chiba volunteers** — Wed 2 Dec 09:30–11:30. Jared still wants parent volunteers.

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
- [x] Class placements confirmed (Toddle 21 Aug): Eldor 6B, Malte 3B, Vega-Lo KA
- [x] Eldor Season 2 CCA allocated (5 Nov): KPASS MS Boys Basketball
