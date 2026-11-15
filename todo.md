# TIS Weekly Briefing — Todo

Next steps. Move done items to decisions.md or delete them.

## Open

- [ ] **Add Gmail API Cloud secrets** (optional) — only if inbox search from cloud is needed. `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`.
- [ ] **Decide whether the email replaces `TIS-Summary-print.html`** — `email/weekly-briefing.html` now covers the same content and also prints cleanly. The old print sheet uses CSS Grid/Flexbox and is not email-safe. Delete it once confirmed.
- [ ] **Verify bus situation** — Bus requests were removed from re-enrolment (March 2026). Confirm if bus is still needed for any child.
- [ ] **Update memory.md with House Team colours** — Sheet published 16 Sep; colours not extracted (needs login).
- [ ] **Reply to Stephen Richards** — Vega-Lo brand video consent + drop-off parent by Mon 16 Nov. Filming 8–10 Dec.
- [ ] **Follow up with Makoto** — Eldor Tuesday 07:00 basketball vs Monday ice hockey; activity change still unanswered.
- [ ] **Confirm Scott d’Aquin** — Sofia proposed Tue 17 Nov 12:00–12:50 for Eldor math; Scott has not confirmed.
- [ ] **Eldor English novel** — finish by Mon 23 Nov (school holiday).

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
- [x] LS Season 2 CCA allocated (13 Nov): Malte Sewing Wed 15:30; Vega-Lo Kids-4-Kids Fri 15:30
- [x] G3 Amazon Chiba volunteers — G3 News 13 Nov thanked volunteers; trip Wed 2 Dec 09:30–11:30
- [x] Sunday 8 Nov 2026 briefing filled for 9–15 Nov and sent via Resend
- [x] Sunday 15 Nov 2026 briefing filled for 16–22 Nov and sent via Resend (`01a1deaa-a57c-76e9-a99d-85aa37a1e96d`)
