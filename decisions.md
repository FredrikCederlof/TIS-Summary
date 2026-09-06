# TIS Weekly Briefing — Decisions

Log of choices made and why.

## 2026-09-06 — Sunday send used Gmail search + Resend CC

Gmail MCP was registered this run and searched the last 14 days (including trash). Campus closure for Mon 7 Sep arrived the same afternoon from Dan Reynolds (Toddle) and Makoto (SchoolsBuddy). Portal HTTP login fields `username-38` / `form_id` were not on the landing page; inbox + memory were enough to fill the template. `scripts/resend_briefing.py` on main still lacked `--cc` and the Cloudflare User-Agent that previous successful sends used, so both were restored before send. Filled HTML for **7–13 Sep 2026**. Sent via Resend to kotolynski@gmail.com, CC sternersofia@gmail.com, id `fe24a81a-2806-4ab5-b951-a0e76fbd3bcb`.

## 2026-08-20 — Cloud Sunday run did not send (Gmail MCP missing)

The replacement Sunday automation (`TIS Sunday parent briefing`, cron `0 10 * * 0`) cloned `insight-works/TIS-Summary` with `email/weekly-briefing.html` already filled for **24–30 Aug 2026**. The Gmail plugin artifact was present, but Cursor did not register an MCP server named `gmail`. Portal login (skip honeypot) and public key dates confirmed Opening Ceremony 24 Aug and first school day 25 Aug. Latest TIS Times on the portal was still 17 Jun 2026.

**Decision:** follow AGENTS.md literally — do not send a markdown or plain-text briefing. Leave the HTML on disk.

**Follow-up (same day):** Fredrik confirmed he had already connected Google Mail on the automation and signed in. Re-login is not the fix. Gmail OAuth Playground was painful (`redirect_uri_mismatch`). **Decision:** preferred cloud send is Resend (`scripts/resend_briefing.py` + `RESEND_API_KEY`). Gmail API scripts remain optional. Desktop `/tis-week` via Gmail MCP remains valid. Resend does not search the inbox; portal + memory fill the briefing.

**Also confirmed from portal-linked docs this run:** no car drop-off at Takanawa; Times Parking P2 with a 30-minute office ticket; Opening Ceremony is standing-room, QR confirmation on the phone.

---

## 2026-08-20 — Sunday email must be the HTML template

The first Sunday automation emailed a markdown recap ("Do this first" bullets) because (1) the prompt said "send a summary" without naming the template, (2) `SKILL.md` told the agent not to send email and to write a chat recap, and (3) `email/weekly-briefing.html` was not on `origin/main`, so a cloud clone had nothing to fill. Fix: `AGENTS.md` in the repo is the send contract; the skill now requires Gmail `htmlBody` = the filled template; the Sunday prompt must say so explicitly.

**Per-child order:** Eldor, Malte, Vega-Lo. Cards have no gray outline — elevation is tonal fill only.

---

## 2026-08-20 — HTML email briefing

**New artifact: `email/weekly-briefing.html`**
Added a Material Design 3 HTML email as a second rendering of the weekly briefing, alongside the canvas. Built from the visual language of a supplied reference design: soft lavender hero, indigo primary, rounded cards, coloured circular icon badges, date badges, and a coloured spine on each timeline day.

Content is a full port of `TIS-Summary-print.html` — all 7 parent actions, all 12 week-at-a-glance rows, the Monday hour-by-hour schedule, all 3 child cards, daily life, upcoming events, all 6 quick links, all 6 contacts, and the sources block. Nothing was dropped. The Monday rows were consolidated into one card with a nested schedule, which preserves every detail while cutting the timeline from 12 rows to 8.

**Table-based layout, inline styles**
Not a preference — a requirement. Outlook renders with the Word engine (no flexbox or grid) and Gmail strips `<style>` in some contexts. The previous `TIS-Summary-print.html` used CSS Grid and Flexbox and would have collapsed in both clients. That file is a print sheet, not an email, and is now superseded.

**Text-first, with per-child avatars as the single exception** *(revised 20 Aug 2026)*
Originally the email was deliberately image-free: Fredrik asked to remove the generated hero illustration, and pure HTML text is the stronger engineering position because mail clients block remote images by default, so an illustration-dependent hero is broken on first open for most recipients.

That still holds for decoration, and hierarchy is still carried by typography, tonal colour and spacing rather than imagery. The rule was relaxed once, for the three per-child avatars in `email/assets/`, because a photo of your own child is content rather than ornament and is the fastest possible way to identify whose card you are reading.

Constraints that keep the exception safe:

- Circle and white ring are **baked into each PNG** with transparent corners, so they render as circles even in Outlook, which ignores `border-radius`. The CSS radius is belt-and-braces.
- Assets are 128px for a 64px display box, roughly 25 KB each.
- Each `<img>` carries the child's name as alt text, so a blocked image degrades to the name, not a blank box.
- `src` is relative for local preview and **must be rewritten to absolute https:// URLs, or attached as CID parts, before sending.** Relative paths resolve to nothing in a mail client.

Do not add further images without meeting the same four conditions.

**Equal-height cards via the cell, not a nested table**
`height:100%` on a table nested inside a `<td>` does not resolve against an auto-height cell, so paired cards rendered ragged. Making the `<td>` itself the card fixes this structurally, since cells in a row are equal height by definition. Requires `box-sizing:border-box` at the mobile breakpoint because those cells now carry padding.

**Rationale**
The canvas is for reading beside chat; the email is for sending, forwarding to a partner, or printing. Same data, two surfaces, each built to its own medium's constraints.

---

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
