# Recording Workflow

Use the simplest reliable renderer that matches the project. Do not force every
animation into one tool.

## 1. Prepare the scene

- Choose a fixed viewport: `1280x720`, `1920x1080`, `1080x1920`, or the target
  embed ratio.
- Load fonts locally or through a stable URL.
- Avoid random values, network-dependent layout, and infinite-only animations.
- Add a way to render by time or frame when possible, for example:
  - `?t=0.0`, `?t=1.5`, `?frame=42`;
  - a global `window.renderAt(timeSeconds)`;
  - a deterministic CSS variable such as `--progress`.

## 2. Preview before recording

Check:

- first frame;
- one middle frame per storyboard beat;
- final frame;
- desktop fit;
- mobile fit if the video will be embedded responsively.

## 3. Export options

### HyperFrames

Use for agent-native HTML-to-video work where the whole deliverable is a video.
Keep the HTML scene clean and make the final output readable without relying on
chat context.

### Remotion

Use when the animation can be a React video composition. Keep scenes split into
small components and render the final composition to MP4/WebM.

### html5-animation-video-renderer

Use when the animation can be rendered deterministically by frame/time. This is
better than screen recording for precise concept videos because it can avoid
dropped frames.

### Playwright + ffmpeg fallback

Use when there is no dedicated renderer.

Basic pattern:

```bash
mkdir -p frames
# Use Playwright to open the HTML scene, set viewport, step through frames,
# capture PNG screenshots into frames/%05d.png.
ffmpeg -y -framerate 30 -i frames/%05d.png -c:v libx264 -pix_fmt yuv420p out.mp4
```

The Playwright script should fail loudly if text overflows, the canvas is
blank, or a required asset is missing.

## 4. Embed in a web page

For short looped concept demos:

```html
<video
  src="/media/concept-demo.mp4"
  poster="/media/concept-demo-poster.jpg"
  muted
  autoplay
  loop
  playsinline
></video>
```

For longer knowledge clips:

```html
<video
  src="/media/lesson.mp4"
  poster="/media/lesson-poster.jpg"
  controls
  playsinline
></video>
```

Add a text summary or transcript near the video when the content teaches a
concept that users may want to scan without watching.

