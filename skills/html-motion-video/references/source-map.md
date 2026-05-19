# HTML Motion Video Source Map

These projects are useful references when building HTML/CSS/JS animation that
can become a polished explainer or concept video.

## Agent-native video pipeline

- [heygen-com/hyperframes](https://github.com/heygen-com/hyperframes)
  - Use when an agent should write HTML and render video in one workflow.
  - Best for: social videos, short explainers, polished generated media.

## Programmatic video from web components

- [remotion-dev/remotion](https://github.com/remotion-dev/remotion)
  - Use when the project can be React-first and the output is truly a video.
  - Best for: repeatable video templates, captions, rendered explainers.

## Premium HTML/CSS/SVG animation

- [greensock/GSAP](https://github.com/greensock/GSAP)
  - Use for timeline-heavy, high-control motion.
  - Best for: premium PPT-like sequences, scroll/camera motion, SVG diagrams.

- [juliangarnier/anime](https://github.com/juliangarnier/anime)
  - Use for compact DOM/SVG animation without a large framework.
  - Best for: concept demos, staged reveals, lightweight motion.

- [motiondivision/motion](https://github.com/motiondivision/motion)
  - Use for modern web animation patterns and small interface motion.
  - Best for: smooth UI transitions, WAAPI-style motion, React/JS web apps.

## CSS-first motion

- [ingram-projects/animxyz](https://github.com/ingram-projects/animxyz)
  - Use for composable CSS animation utilities.
  - Best for: quick slide-like entrances, emphasis, and simple sequences.

- [animate-css/animate.css](https://github.com/animate-css/animate.css)
  - Use for familiar CSS animation classes.
  - Best for: fast prototypes and low-risk entrance effects.

## Directed timeline authoring

- [theatre-js/theatre](https://github.com/theatre-js/theatre)
  - Use when keyframe direction matters and the scene benefits from a studio-like
    timeline.
  - Best for: cinematic concept demos, camera movement, 3D/web hybrid scenes.

## Raw HTML recording

- [dtinth/html5-animation-video-renderer](https://github.com/dtinth/html5-animation-video-renderer)
  - Use when an HTML5 animation needs deterministic frame-by-frame video
    rendering.
  - Best for: canvas/DOM scenes that can expose a frame/time control surface.

## Selection Matrix

| Need | Prefer |
|---|---|
| Fast CSS-only slide effect | AnimXYZ or Animate.css |
| Premium concept animation | GSAP |
| Lightweight DOM/SVG demo | Anime.js |
| App-like UI motion | Motion |
| Timeline/keyframe direction | Theatre.js |
| React-first video | Remotion |
| Agent writes and renders video | HyperFrames |
| Deterministic raw HTML export | html5-animation-video-renderer or Playwright + ffmpeg |

