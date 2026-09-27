# TIS Weekly Briefing — Todo

Next steps. Move done items to decisions.md or delete them.

## Open

- [ ] **Add Gmail API Cloud secrets** (optional) — only if inbox search from cloud is needed. `GMAIL_CLIENT_ID`, `GMAIL_CLIENT_SECRET`, `GMAIL_REFRESH_TOKEN`.
- [ ] **Decide whether the email replaces `TIS-Summary-print.html`** — `email/weekly-briefing.html` now covers the same content and also prints cleanly. The old print sheet uses CSS Grid/Flexbox and is not email-safe. Delete it once confirmed.
- [ ] **Verify bus situation** — Bus requests were removed from re-enrolment (March 2026). Confirm if bus is still needed for any child.
- [ ] **Update memory.md with House Team colours** — G3 list circulated 25 Sep; spreadsheet still needs a logged-in extract.
- [ ] **Sports Days** — Vega-Lo Tue 13 Oct 13:15–15:00 on campus; Malte Fri 16 Oct 09:40–13:40 at YCAC. House-colour shirts. Cancel after-school bus if picking up from the venue.
- [ ] **Eldor Explorations packing** — G6–8 trip 12–15 Oct, Mountain Park Tsunan. Assembly with JUMP! Mon 5 Oct. Fri 16 Oct starts 09:00.
- [ ] **Vega-Lo family + baby photos** — Email Claudia this week if not already sent (KA Who We Are).
- [ ] **School photo order forms** — Coming home week of 28 Sep. Tell the office if missing.
- [ ] **K4K Fluffy Day Fri 9 Oct** — ¥100 donation.

## Done

- [x] Gmail MCP connected and tested (Aug 2026); cloud Sunday search worked 21 Aug–27 Sep 2026
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
- [x] Sunday automation prompt now names the HTML template (20 Aug 2026)
- [x] Gmail API fallback scripts (`scripts/gmail_briefing.py`, `gmail_oauth_setup.py`) (20 Aug 2026)
- [x] Resend send script (`scripts/resend_briefing.py`) as preferred cloud path (20 Aug 2026)
- [x] **Resend Cloud secret** injected; Sunday HTML sends 21 Aug through 20 Sep 2026
- [x] **Class placements** — Eldor 6B, Malte 3B, Vega-Lo KA (Toddle 21 Aug)
- [x] **Class teachers** — Chrissy / Jared+Sarah / Claudia+Laura
- [x] **CCA Season 1 allocations** — soccer / basketball / Tinker Lab (SchoolsBuddy 28 Aug)
- [x] **Kiwi Kitchen** — first-day deadline has passed; keep account if using lunch

## Superseded (moved from Open)

- [x] Opening-week emergency-contact / first-day kit items — no longer this week's actions
