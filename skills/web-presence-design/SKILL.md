---
name: web-presence-design
description: Use when building or improving beautiful marketing websites, official sites, course landing pages, customer case-study pages, portfolio pages, or SaaS/product landing pages. Combines taste control, information architecture, page-specific conversion structure, real brand assets, implementation, and visual verification.
---

# Web Presence Design

Use this skill when the user wants a polished public-facing website rather than
a generic web app screen: official site, product homepage, course page, customer
case page, portfolio, agency site, SaaS landing page, launch page, or marketing
microsite.

## Core Stance

Build a web presence, not a template.

```text
brand truth -> audience promise -> information architecture -> visual direction -> implementation -> screenshot review
```

Do not start from a component library. Start from what the page must make the
visitor believe, feel, understand, and do.

## Relation To Other Skills

- Use `huashu-design` for HTML prototypes, visual experiments, motion demos,
  slides, and high-fidelity design exploration.
- Use `html-motion-video` when a page needs knowledge explainer videos,
  concept demonstration clips, or slide-deck-like HTML/CSS/JS motion recorded
  into video.
- Use this skill for production-grade marketing websites and page systems.
- Use `platform-writing` when the output is an article or document rather than a
  website.

## Workflow

1. **Classify the surface.**
   Pick one primary page type:
   - official/product site;
   - course landing page;
   - customer case-study page;
   - portfolio/agency site;
   - SaaS/product launch page.

2. **Collect context and assets.**
   For a concrete brand or product, verify current facts and collect real
   assets before designing: logo, product screenshots/renders, course cover,
   teacher photo, customer logo, customer quote, metrics, screenshots, and
   brand colors. If core assets are missing, use honest placeholders only while
   making the gap visible.

3. **Write the page promise.**
   Before layout, write:
   - audience;
   - one-sentence promise;
   - primary conversion action;
   - trust proof;
   - what the user should remember after leaving.

4. **Choose a visual direction.**
   Pick one clear direction and commit:
   - premium SaaS: calm, precise, product-led, strong proof;
   - editorial: image-led, typographic, narrative;
   - education: warm, structured, progress-oriented;
   - customer proof: credible, specific, result-first;
   - creative studio: bolder composition and stronger art direction.

5. **Build from structure, then craft.**
   Use the project stack and components when present. For new React/Next work,
   default to Next.js or React, Tailwind, shadcn/Radix-compatible components,
   and icons from the project's existing icon set. Do not import packages before
   checking `package.json`.

6. **Verify visually.**
   Run the site, capture at least desktop and mobile screenshots, check console
   errors, check overflow, and inspect the first viewport. If the page is meant
   to sell or teach, verify the first viewport contains the brand/product and a
   clear next action.

## Page Patterns

Read `references/page-patterns.md` when choosing sections for official sites,
course pages, or customer case studies.

Read `references/source-map.md` when deciding which external skill/template
patterns to borrow.

## Anti-Slop Rules

- No default purple/blue AI gradient hero.
- No generic three-card feature row as the whole page.
- No fake metrics, fake testimonials, or anonymous customer quotes when the
  page depends on trust.
- No product page without product signal in the first viewport.
- No course page without learning outcome, teacher credibility, curriculum, and
  proof.
- No customer case page without before/after, concrete numbers, customer
  context, and implementation story.
- No decorative image if a real logo, screenshot, product photo, or customer
  artifact is available.

## Output Contract

For non-trivial pages, produce:

1. page type and promise;
2. section plan;
3. implementation changes;
4. screenshots or preview path;
5. what remains to polish if assets or facts are missing.

If the work becomes a reusable pattern, preserve the lesson as memory, skill,
methodology, and impression rather than only shipping code.
