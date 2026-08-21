# TIS Weekly Briefing — Todo

Next steps. Move done items to decisions.md or delete them.

## Open

- [ ] **Add Resend Cloud secret** — `RESEND_API_KEY` (Runtime Secret) at https://cursor.com/dashboard/cloud-agents then re-run Sunday. Optional `RESEND_FROM` after domain verify. This is the intended cloud send path.
- [ ] **Add Gmail API Cloud secrets** (optional) — only if inbox search from cloud is needed. `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`.
- [ ] **Decide whether the email replaces `TIS-Summary-print.html`** — `email/weekly-briefing.html` now covers the same content and also prints cleanly. The old print sheet uses CSS Grid/Flexbox and is not email-safe. Delete it once confirmed.
- [x] **Confirm Eldor's and Malte's class placements** — Toddle 21 Aug 2026: Eldor 6B (Chrissy Erwin, 112), Malte 3B (Jared Barnes, 216), Vega-Lo KA (Claudia Ackermann + Laura, 202).
- [ ] **Verify bus situation** — Bus requests were removed from re-enrolment (March 2026). Confirm if bus is still needed for any child.
- [ ] **Kiwi Kitchen account** — Create account before Tue 25 Aug if using school lunch. Mention grade + A or B for first order.
- [ ] **Update memory.md with House Team colours** — Assigned in first full week of school (week of 25 Aug). Add once known.
- [x] **Update memory.md with class teachers** — Eldor: Chrissy Erwin; Malte: Jared Barnes; Vega-Lo: Claudia Ackermann + Laura.
- [ ] **Hopes & Dreams forms** — Complete three Google Forms and bring copies Fri 28 Aug (Malte 08:15, Vega-Lo 08:45, Eldor 09:15).
- [ ] **PYP Choir for Malte** — Permission slip to Yui, PYP Music Room 1st floor, by Fri 5 Sep if he wants to join.
- [ ] **SchoolsBuddy CCA allocation result** — Check before Mon 31 Aug and note which activities each child was allocated.

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
