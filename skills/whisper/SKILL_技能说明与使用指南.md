---
name: whisper
description: OpenAI's speech recognition model for audio transcription and translation. Supports 99 languages, local CPU/GPU inference. Use when converting audio/video to text, transcribing Chinese content, or extracting speech from media files.
version: "1.1.0"
metadata:
  yao_category: "AI内容"
  hermes:
    tags: ["audio", "transcription", "speech-recognition", "openai"]
---

# OpenAI Whisper — Speech Recognition

> Local audio transcription and translation, supports 99 languages including Chinese.

## Overview

Whisper is OpenAI's open-source speech recognition model. Runs locally on CPU (small/medium models) or GPU (large models). Perfect for:
- Transcribing audio/video files to text
- Extracting Chinese speech content
- Translating non-English audio to English text

## Installation

```bash
# Install whisper in the project venv
pip install -U openai-whisper

# Install ffmpeg for audio processing
apt-get install -y ffmpeg  # or: yum install -y ffmpeg
```

## Available Models

| Size | Parameters | English-only | Disk | RAM (CPU) | Speed (RTF) |
|------|-----------|-------------|------|-----------|-------------|
| tiny | 39 M | ✓ | 75 MB | ~0.5 GB | ~32x |
| base | 74 M | ✓ | 142 MB | ~1 GB | ~16x |
| **small** | 244 M | ✓ | 461 MB | ~2 GB | ~6x |
| medium | 769 M | ✓ | 1.5 GB | ~4 GB | ~2x |
| large | 1550 M | ✗ | 2.9 GB | ~6 GB | ~1x |

**For 2GB server**: use `small` or `base` model. `small` gives good Chinese accuracy with swap support.

## Usage

### Python API

```python
import whisper

# Load model (downloads on first use)
model = whisper.load_model("small")

# Transcribe audio file
result = model.transcribe("audio.mp3", language="zh")
print(result["text"])

# Translate to English (from any language)
result = model.transcribe("audio.mp3", language="zh", task="translate")
print(result["text"])
```

### CLI

```bash
# Transcribe
whisper audio.mp3 --model small --language zh --output_dir ./output

# Translate to English
whisper audio.mp3 --model small --language zh --task translate

# Output formats: txt, srt, vtt, tsv, json
whisper audio.mp3 --model small --output_format srt
```

### With Video Files

```python
import whisper
from moviepy.editor import VideoFileClip

# Extract audio from video
video = VideoFileClip("video.mp4")
video.audio.write_audiofile("audio.mp3")

# Transcribe
model = whisper.load_model("small")
result = model.transcribe("audio.mp3", language="zh")
```

## Error Handling

### Common Errors and Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| `FileNotFoundError: ffmpeg` | ffmpeg not installed | `apt-get install -y ffmpeg` |
| `RuntimeError: CUDA out of memory` | GPU VRAM insufficient | Use `device="cpu"` or smaller model |
| `OSError: [Errno 12] Cannot allocate memory` | RAM exhausted | Enable swap, use `base` model, set `OMP_NUM_THREADS=1` |
| `URLError/Timeout` | Model download failed | Pre-download: `whisper --model small --help`, use proxy |
| `ValueError: Invalid language` | Unsupported language code | Check [supported languages](https://github.com/openai/whisper#available-models-and-languages) |
| `RuntimeError: Error(s) in loading state_dict` | Corrupted cache | Delete `~/.cache/whisper/` and retry |

### Robust Transcription Pattern

```python
import whisper
import os
import torch

def safe_transcribe(audio_path, model_name="small", language="zh"):
    """Transcribe with comprehensive error handling."""
    # Validate input
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")
    
    # Check ffmpeg availability
    import shutil
    if not shutil.which("ffmpeg"):
        raise RuntimeError("ffmpeg not found. Install: apt-get install -y ffmpeg")
    
    # Setup environment for low-memory systems
    os.environ["OMP_NUM_THREADS"] = "1"
    os.environ["MKL_NUM_THREADS"] = "1"
    
    # Choose device
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    try:
        model = whisper.load_model(model_name, device=device)
        result = model.transcribe(audio_path, language=language)
        return result["text"]
    except RuntimeError as e:
        if "CUDA out of memory" in str(e):
            print("GPU OOM, falling back to CPU...")
            torch.cuda.empty_cache()
            model = whisper.load_model(model_name, device="cpu")
            result = model.transcribe(audio_path, language=language)
            return result["text"]
        raise
```

### Batch Processing with Error Recovery

```python
import whisper
import glob
import os

model = whisper.load_model("small", device="cpu")
success, failed = [], []

for audio_file in glob.glob("*.mp3"):
    try:
        result = model.transcribe(audio_file, language="zh")
        out = audio_file.replace(".mp3", ".txt")
        with open(out, "w") as f:
            f.write(result["text"])
        success.append(audio_file)
    except Exception as e:
        failed.append((audio_file, str(e)))
        print(f"FAILED {audio_file}: {e}")

print(f"Done: {len(success)} succeeded, {len(failed)} failed")
```

## Memory Management (2GB Server)

```python
import torch
import whisper

# Free GPU memory if available
if torch.cuda.is_available():
    torch.cuda.empty_cache()

# Use CPU with limited threads
import os
os.environ["OMP_NUM_THREADS"] = "2"

model = whisper.load_model("small", device="cpu")
```

## Chinese Transcription Tips

1. **Use `--language zh`** — explicitly set language for better accuracy
2. **small model** — best balance of accuracy vs memory for Chinese
3. **long audio** — whisper auto-segments, but pre-splitting >30min files helps
4. **swap support** — on 2GB server, ensure 4GB+ swap available (already configured)

## Integration Examples

### 抖音视频转文字
```python
import whisper
import subprocess

# Extract audio from video file
subprocess.run(["ffmpeg", "-i", "input.mp4", "-vn", "-acodec", "mp3", "audio.mp3"])

# Transcribe in Chinese
model = whisper.load_model("small")
result = model.transcribe("audio.mp3", language="zh")
print(result["text"])
```

## Notes

- Models are cached at `~/.cache/whisper/` (~461 MB for small)
- First run downloads the model (requires network)
- On 2GB server with 6GB swap, small model works but may use swap
- Base model (~142 MB) is faster and lighter if Chinese accuracy is acceptable
