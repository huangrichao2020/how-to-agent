---
name: html-motion-video
description: Use when building HTML/CSS/JS animated explainer videos, concept demonstration videos, course clips, product mechanism demos, or website sections that need embedded motion with a polished slide-deck feel.
---

# HTML Motion Video

Use this skill when a page should teach through motion: knowledge explainers,
concept demos, product mechanism videos, architecture walkthroughs, course
fragments, or animated sections that can also be recorded as MP4/WebM.

## Core Stance

Make the web page behave like a refined slide deck with a camera, not like a
random animated landing page.

```text
teaching point -> storyboard beats -> visual metaphor -> timeline animation -> recorded video -> embedded lesson
```

Motion is useful only when it explains causality, sequence, contrast, state
change, hierarchy, or attention. Decorative movement is not enough.

## When To Use

- The user asks for a knowledge explanation video, concept animation, course
  demo, or animated web lesson.
- A website needs embedded short videos that explain a mechanism instead of
  only showing static cards.
- A complex idea would be easier to understand as staged reveal, before/after,
  flow, zoom, morph, split, merge, or timeline.
- The requested quality target feels like a good Keynote/PPT presentation:
  clear scenes, elegant typography, deliberate transitions, and useful pauses.

## Source Map

Read `references/source-map.md` before choosing libraries.

The default stack choices are:

- `GSAP` for premium timeline control over HTML/CSS/SVG.
- `Anime.js` for lighter DOM/SVG motion and compact concept demos.
- `Motion` / `Motion One` style animation for small WAAPI-driven interface
  motion.
- `AnimXYZ` or `Animate.css` for quick CSS-only entrances and simple sequences.
- `Theatre.js` when the animation needs keyframed direction like a motion
  design timeline.
- `Remotion` when the project can be React-first and video is the primary
  output.
- `HyperFrames` when an agent should write HTML and render video as one
  pipeline.
- `html5-animation-video-renderer` or Playwright plus ffmpeg when raw HTML/CSS
  needs deterministic frame capture.

## Workflow

1. **Name the lesson.**
   Write one sentence:
   - what the viewer should understand;
   - what misconception or confusion the animation removes;
   - what should remain in memory after watching.

2. **Storyboard 3-7 beats.**
   Each beat is one slide-like state:
   - setup;
   - reveal;
   - transition;
   - contrast or cause;
   - conclusion;
   - optional call to action.

3. **Choose the visual grammar.**
   Pick one primary grammar:
   - staged text reveal for definitions;
   - node/link flow for systems and dependency graphs;
   - timeline for historical or process explanations;
   - zoom and layering for abstraction levels;
   - morphing shapes for state transitions;
   - split-screen compare for before/after;
   - cursor/camera walkthrough for product usage.

4. **Build deterministic HTML.**
   Use fixed scene dimensions for video, usually `1280x720`, `1920x1080`, or a
   matching vertical format. Keep fonts loaded, random values seeded or absent,
   animation durations explicit, and layout stable. Text must remain readable
   in every frame.

5. **Animate by timeline, not vibes.**
   Prefer a named timeline with beat labels:
   - `intro`;
   - `define`;
   - `showMechanism`;
   - `compare`;
   - `conclude`.

   The timeline should make it easy to seek, replay, record, and adjust.

6. **Record or render.**
   Prefer the simplest reliable path for the project:
   - HyperFrames for agent-native HTML video generation;
   - Remotion for React video components;
   - html5-animation-video-renderer for frame-by-frame HTML animation export;
   - Playwright screenshots plus ffmpeg when no dedicated renderer fits.

   See `references/recording-workflow.md`.

7. **Embed with care.**
   In websites, embed the result with a poster frame, captions or transcript
   when useful, and proper responsive sizing. Autoplay should be muted and loop
   only for short ambient concept demos. Longer knowledge clips should expose
   controls.

8. **Verify like a designer.**
   Check first frame, last frame, a middle frame, mobile fit, desktop fit,
   console errors, and whether the animation actually explains the lesson
   better than a static diagram.

## Output Contract

For non-trivial work, produce:

1. the lesson sentence;
2. storyboard beats;
3. chosen animation stack and why;
4. implementation path;
5. recorded video path or explicit render command;
6. embed instructions;
7. verification notes.

## Anti-Slop Rules

- No animation without a teaching job.
- No generic spinning shapes, floating blobs, or motion that only decorates.
- No text that moves so fast the viewer cannot read it.
- No layout shifts during recording.
- No uncontrolled randomness in recorded explainers.
- No video export without checking at least first, middle, and final frames.
- No long raw tool trace in the final user-facing card; explain the outcome in
  human terms and keep technical trace secondary.

