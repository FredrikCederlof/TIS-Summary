# TIS Weekly Briefing — Decisions

Log of choices made and why.

## 2026-08-20 — Material Design 3 design system

**Canvas design language: Material Design 3**
Adopted MD3 as the primary design language for the TIS-Summary canvas. Key choices:
- Tonal surface containers (`fill.primary/secondary/tertiary/quaternary`) replace flat cards and decorative borders
- Child identity expressed through full color-container banners (`category.green/blue/pink` per child)
- No `box-shadow` — elevation via tonal fills only (aligns with both MD3 and canvas SDK constraints)
- 8px spacing base, M3 typography hierarchy (SectionLabel → H2 pattern), active Pill chips

**Cursor rules added**
- `.cursor/rules/canvas-design-system.mdc` — scoped to `*.canvas.tsx`, defines all M3 primitives, color roles, layout conventions, and the pre-delivery checklist
- `.cursor/rules/project-workflow.mdc` — always on, defines the knowledge file protocol and definition of done

**Rationale**
Fredrik requested premium SaaS-quality UI comparable to Google Workspace / Linear. MD3 is the correct foundation for a school briefing tool — structured, accessible, expressive without being decorative. The canvas SDK constraints (no shadows, no animations, no external imports) are compatible with MD3's philosophy of tonal elevation over shadow elevation.

---

## 2026-08-20 — Initial build

**Canvas over plain chat**
Briefing is a standalone analytical artifact (timeline, actions, tables). Canvas renders it as a proper dashboard beside chat.

**Canvas filename: `TIS-Summary.canvas.tsx`**
Descriptive, stable name. Overwritten each run so there is always exactly one file.

**Skill location: `~/.cursor/skills/tis-weekly-briefing/`**
Personal skill (not project-scoped) so it is available across all workspaces, not just this one.

**Command: `/tis-week`**
Short, memorable, unambiguous. Maps to `~/.cursor/commands/tis-week.md`.

**Dedup strategy: merge by event + date + action**
The same announcement arrives up to 3× (one per child). Showing it once reduces noise without losing information. Child-specific items (placement, form, supply list) are still listed per child.

**Portal credentials stored in `memory.md`**
Avoids re-prompting every run. Credentials are for a shared read-only parent account (`parent` / `inspire`), not personal.

**Automation: Sunday 19:00**
Gives a full weekend evening briefing before the school week. Japan time (JST = UTC+9). Draft created, not yet saved — Fredrik needs to confirm cron time in the Automations editor.

**Knowledge split into four files**
`memory.md` (facts) / `architecture.md` (structure) / `decisions.md` (rationale) / `todo.md` (next steps). New agents read only these four files to bootstrap without loading full conversation history.
