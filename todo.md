# TIS Weekly Briefing — Todo

Next steps. Move done items to decisions.md or delete them.

## Open

- [ ] **Decide whether the email replaces `TIS-Summary-print.html`** — `email/weekly-briefing.html` now covers the same content and also prints cleanly. The old print sheet uses CSS Grid/Flexbox and is not email-safe. Delete it once confirmed.
- [ ] **Commit and push `email/` + `AGENTS.md` to origin** — the Sunday cloud agent clones `insight-works/TIS-Summary`. Until these files are on `main`, it cannot fill the template.
- [ ] **Replace the Sunday automation** — current prompt produced a plain-text recap. New one must fill `email/weekly-briefing.html` and send it as Gmail `htmlBody`. Cron `0 10 * * 0` (UTC = 19:00 JST). Delete or disable the old automation after the replacement is saved.
- [ ] **Confirm Eldor's and Malte's class placements** — Toddle opens Fri 21 Aug. Run `/tis-week` after that date to capture placements in the next canvas.
- [ ] **Verify bus situation** — Bus requests were removed from re-enrolment (March 2026). Confirm if bus is still needed for any child.
- [ ] **Kiwi Kitchen account** — Create account before Tue 25 Aug if using school lunch. Mention grade + A or B for first order.
- [ ] **Update memory.md with House Team colours** — Assigned in first full week of school (week of 25 Aug). Add once known.
- [ ] **Update memory.md with class teachers** — Available on Toddle from Fri 21 Aug.
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
