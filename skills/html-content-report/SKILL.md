---
name: html-content-report
description: Use when turning a content artifact — design plan, judgment report, XHS/social-media post preview, editorial deliverable, or content-rich one-pager — into a single self-contained HTML+CSS file that is shareable as a link, easy to read on desktop and mobile, and visually polished without external dependencies. Heavier than Markdown, lighter than a prototype.
---

# HTML Content Report

Use this skill when the deliverable is **content-shaped** (a plan, a report, a
visual preview, a publish-ready copy package) and the user wants something
better than a Markdown file but doesn't need an interactive React app, a
slide deck, or a marketing site.

The output is **one self-contained `.html` file** with embedded CSS, no
build step, no external CDN, no JavaScript frameworks. Open it in any
browser and it works.

## When To Use

- "把这个 XHS 图文方案做成 HTML 预览"
- "做一个 X 主题的视觉方案 HTML 报告"
- "把这份内容/清单/对比做成可分享的网页"
- "做一份小而精的报告（不用框架）"
- "Make this into a polished single-file HTML"

## When NOT To Use

- Public marketing site, course page, product landing → `web-presence-design`
- High-fidelity prototype with interactions / motion / slides → `huashu-design`
- Knowledge explainer video / motion demo → `html-motion-video`
- Just a long-form article or document → Markdown or `platform-writing`

## Relation To Other Skills

- `web-presence-design` produces Next.js/React production sites; this skill
  is the static-HTML counterpart for content-shaped deliverables.
- `huashu-design` is for prototypes and visual exploration; this skill is
  for finished, shareable, content-heavy artifacts.
- `html-motion-video` adds video; this skill stays text + image + card.
- `platform-writing` is article-shaped; this skill is multi-section
  report-shaped with strong visual hierarchy.

## Core Stance

Define the design tokens first. Then build the section structure. Then
add the visual craft. Tokens + structure lock the look; craft makes it
feel premium.

```text
purpose + audience
  -> design tokens (color, type, spacing)
  -> 7-section structure
  -> component recipes (sticky nav, hero, cards, accordion, ...)
  -> craft (hover, transition, polish)
  -> browser self-test
```

## Dependencies (Skills, Tools, Inputs)

This skill is the **visualization layer**. It produces a beautiful HTML
container, but the **content** comes from upstream skills and the
**production** runs on specific runtime tools. Be explicit about which is
which so the next run can be replicated or replaced.

### Upstream skills (where the content comes from)

- **Domain-specific plan skill** — produces the structured plan, prompt
  list, publishing copy, review checklist, etc. Examples:
  - `xhs-visual-director-skill` (xiaohongshu post plans)
  - `xhs` / `wechat` / `medium` / `linkedin` equivalents
  - a product analysis skill that emits "3 plans / 4 dimensions /
    8 steps" structure
  - any skill whose output is a sectioned plan or report
  Treat that skill's output as the source of truth for sections 4-7.
  Do not invent new content; render what the upstream skill already
  produced.
- **Style system docs** (optional) — for the design system section, the
  5-6 swatch colors should come from the upstream skill's style catalog
  if it has one. `xhs-visual-director-skill` ships a 22KB
  `docs/style_system.md` that defines the visual palette; this skill
  reads it and renders swatches.

### Runtime tools (what produces the file)

- `execute_code` (Python sandbox) — for fetching reference HTML, parsing
  remote docs (e.g. GitHub raw content via API), generating token
  variants, batch-rendering cards. Not required for simple single-file
  deliverables; required when content is dynamic.
- `write_file` (or equivalent) — the one tool that actually writes the
  final `.html`. The skill output is a complete file body, written in
  one call. Avoid `patch` for the first build; it loses the cohesion.
- `terminal` — for `ls -la` / `wc -l` / `head` self-checks after writing,
  and for opening the file (`open path/to/file.html` on macOS).
- `read_file` — for reading source skill content before rendering, and
  for post-write verification.
- `send_message` with `MEDIA:/absolute/path` — for delivering the file
  to the user through chat. The HTML renders inline as an attachment.

### Inputs the user must provide

- **Topic / purpose** — what is the deliverable about. Required.
- **Audience and primary action** — who reads it, what should they do
  after. Strongly recommended.
- **Reference deliverables (optional)** — links to upstream skill
  outputs, brand guidelines, or examples of what "good" looks like.
- **Constraint budget (optional)** — word count cap, page count cap,
  required sections, languages.

### What this skill does NOT do

- Does not generate images. The phone frames, swatches, and
  illustrations are CSS placeholders that the user can replace with
  real images from MJ / 即梦 / Sora / etc.
- Does not produce new content sections. Sections 4-7 are
  transformations of upstream-skill output, not new writing.
- Does not handle multi-page navigation. One `.html` = one deliverable.
  For multi-page, link to separate files or use a build tool.
- Does not load web fonts or external CSS. Self-contained is the
  contract.

### Dependency map (real example: 杭州美食地图 v2)

```text
xhs-visual-director-skill
  └── (via GitHub raw API) → SKILL.md, docs/style_system.md
        └── (via this skill) → 7 sections
              ├── 1. Sticky nav (anchor links)
              ├── 2. Hero (title + phone frame)
              ├── 3. Design system (swatches from style_system.md)
              ├── 4. 8 phone frames (from upstream 8-page plan)
              ├── 5. 3 plans + 4 dimensions (from upstream judgment)
              ├── 6. Prompt accordion (from upstream 8 prompts)
              └── 7. Publishing copy (from upstream Step 9)
                    │
                    └── write_file → ~/Desktop/xhs-output/hangzhou-food-map-v2.html
                          │
                          └── send_message(MEDIA:...) → delivered to chat
```

## Design Tokens (Default Dark)

Lock these before writing markup. Override only with reason.

```css
:root {
  --bg:        #0A0A0E;   /* deep space, primary surface */
  --bg-2:      #14141A;   /* alt section background */
  --card:      #1A1A22;   /* default card surface */
  --card-2:    #22222C;   /* nested / hover card */
  --border:    #2A2A35;
  --border-2:  #3A3A48;
  --text:      #F5F5F0;
  --text-2:    #B8B8B0;
  --text-3:    #6E6E68;
  --accent:    #C8FF6E;   /* primary action / highlight */
  --warm:      #D4A574;   /* secondary highlight */
  --hot:       #FF6B5C;   /* danger / accent for stamps */
  --cool:      #6BB8FF;   /* tertiary highlight */
}
```

Font stack: `-apple-system, "PingFang SC", "HarmonyOS Sans", "Microsoft YaHei", "Helvetica Neue", sans-serif`. Mono: `"SF Mono", monospace`. Do not load web fonts; system fonts are fast and consistent on the user's machine.

## 7-Section Structure

The default spine. Skip sections, never re-order them.

1. **Sticky top nav** — backdrop-filter blur, brand mark, anchor links to
   every section. The reader always knows where they are.
2. **Hero** — 2 columns: left = eyebrow label + big title + sub copy + meta
   pills, right = a single hero visual (phone frame, mock card, or diagram).
3. **Design system** — color swatches (5-6) + typography sample (4 sizes).
   This is the "constitution" — readers see the rules before the content.
4. **Primary content** — the thing the report is about. 8 phone frames for
   an XHS plan, 12 feature cards for a product analysis, etc. Use
   `aspect-ratio` for 3:4 / 16:9 / 1:1 frames so the visual is real, not
   abstract.
5. **Comparison or judgment** — 3-column plans, 4-dimension judgment cards,
   or a side-by-side diff. Highlight the recommended option with an accent
   border and a "推荐" badge.
6. **Process or rules** — accordion for prompts, checklist for review,
   step list for workflow. Each item is verifiable.
7. **Deliverable copy** — the actual copy the user will publish: titles,
   body, tags, comment, CTA. Show it inside a phone-frame or callout so
   it feels like the artifact, not just text.

## Component Recipes

The patterns that appear in 80% of deliverables. Copy, then adapt.

### Sticky nav

```html
<nav class="nav">
  <div class="nav-inner">
    <div class="nav-brand">···</div>
    <div class="nav-links">
      <a href="#section1">概览</a>
      <a href="#section2">设计</a>
      ...
    </div>
  </div>
</nav>
```

```css
.nav { position: sticky; top: 0; z-index: 50;
       background: rgba(10, 10, 14, 0.85);
       backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
       border-bottom: 1px solid var(--border); }
```

### 3:4 phone frame (XHS / IG preview)

```html
<div class="phone">
  <div class="phone-canvas">
    <span class="phone-tag">01 / 08</span>
    <span class="phone-tag-label">封面</span>
    <h3>标题</h3>
    <ul><li>...</li></ul>
  </div>
</div>
```

```css
.phone-canvas { aspect-ratio: 3 / 4; background: var(--bg-2);
                border-radius: 14px; padding: 20px; }
```

Aspect-ratio + padding + 14px radius is what sells the "phone" feel
without any image asset.

### Accent border for "recommended"

```css
.plan.recommended { border-color: var(--accent); }
.plan-recommend  { position: absolute; top: -10px; right: 16px;
                   background: var(--accent); color: var(--bg);
                   font-size: 10px; font-weight: 700;
                   padding: 4px 10px; border-radius: 999px; }
```

### Left-bar callout (left color bar + content)

```css
.rec-card.use   { border-left: 3px solid var(--accent); }
.rec-card.avoid { border-left: 3px solid var(--hot); }
```

### Accordion for prompts / hidden detail

```html
<details class="prompt" open>
  <summary><span class="prompt-num">Page 01</span>封面</summary>
  <div class="prompt-body">...prompt text...</div>
</details>
```

```css
.prompt-body { background: var(--bg-2); border-top: 1px solid var(--border);
               font-family: "SF Mono", monospace; font-size: 12px; }
```

### Responsive grid breakpoints

Default 4 → 2 → 1:

```css
.phone-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }
@media (max-width: 1100px) { grid-template-columns: repeat(2, 1fr); }
@media (max-width: 560px)  { grid-template-columns: 1fr; }
```

## Workflow

1. **Lock the tokens.** Open the file, paste the `:root` block. If you
   change a color, change it once and propagate. Token drift is the #1
   reason "v2 looks worse than v1".
2. **Place 7 section skeletons.** 7 `<section>` blocks with IDs, empty
   `<div class="wrap">` inside each. The structure is the skeleton; the
   craft fills it in.
3. **Sticky nav second.** Once the section IDs exist, the nav anchors
   become real. Build the nav once and never edit it again.
4. **Hero and design system first.** They define how the rest feels.
5. **Fill the primary content section.** This is usually 60-70% of the
   file. For a content report with 8 items, the 8 cards are the spine.
6. **Comparison + judgment.** 3 plans, 4 dimensions, recommended option
   highlighted. Don't bury the recommendation.
7. **Process rules and deliverable copy.** Accordion + checklist + the
   actual artifact the user will copy out.
8. **Browser self-test.** Open the file. Check first viewport. Check at
   1100px (laptop) and 560px (phone). Check that the back-to-top nav
   works. Check that the accent color is consistent.

## Anti-Slop Rules

- No default purple/blue AI gradient hero.
- No emoji used as the only icon — emoji at most as accent, never as
  primary UI signal.
- No center-aligned everything. Use 2-column or grid layouts.
- No `font-weight: 100` thin text. Use 400 / 600 / 700 / 800.
- No web font loading. System fonts only.
- No JavaScript framework imports. No CDN. No build step.
- No fake data presented as real. Placeholders must look like
  placeholders.
- No "AI template" cliches: "🚀 Supercharge your...", "💡 Unlock...".
- No `aspect-ratio` ignored. Every visual frame should have one.
- No `transition: all` on hover. Specify the property.

## Output Contract

A finished deliverable includes:

1. one self-contained `.html` file at a path the user can name;
2. tokens locked (`:root` block visible at top of `<style>`);
3. sticky nav with anchor links to every section;
4. hero, design system, primary content, comparison, process, deliverable
   sections — at least 5, at most 8;
5. real `aspect-ratio` on every visual frame;
6. responsive: works on 1100px laptop and 560px phone;
7. no console errors, no 404, no missing fonts.

## Real Examples

- `~/Desktop/xhs-output/hangzhou-food-map-v2.html` — 8-page XHS post
  preview with phone frames, design system, 3 style plans, style
  judgment, prompt library, review checklist, and publishing copy.

## Related Patterns

- `references/design-tokens.md` — extended token catalog (light mode,
  monochrome, etc.) — to be added when needed.
- `references/component-snippets.md` — copy-paste component library —
  to be added when needed.
