---
name: songsee
description: Generate spectrograms and audio feature visualizations (mel, chroma, MFCC, tempogram, etc.) from audio files via CLI. Useful for audio analysis, music production debugging, and visual documentation.
version: 1.1.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Audio, Visualization, Spectrogram, Music, Analysis]
    homepage: https://github.com/steipete/songsee
    category: media
prerequisites:
  commands: [songsee]
---

# songsee

Generate spectrograms and multi-panel audio feature visualizations from audio files.

## 触发条件

当用户需要以下场景时触发此 Skill：
- 生成音频频谱图/声谱图
- 可视化音频特征（Mel、Chroma、MFCC 等）
- 对比不同音频文件的频谱差异
- 调试音乐合成或音频处理 pipeline

## Prerequisites

Requires [Go](https://go.dev/doc/install):
```bash
go install github.com/steipete/songsee/cmd/songsee@latest
```

Optional: `ffmpeg` for formats beyond WAV/MP3.

Verify installation:
```bash
songsee --help
```

## 工作流程

### Step 1: 基础频谱图

```bash
songsee track.mp3
```

### Step 2: 指定输出文件

```bash
songsee track.mp3 -o spectrogram.png
```

### Step 3: 多面板可视化网格

```bash
songsee track.mp3 --viz spectrogram,mel,chroma,hpss,selfsim,loudness,tempogram,mfcc,flux
```

### Step 4: 时间切片分析

```bash
# 从 12.5s 开始，持续 8s
songsee track.mp3 --start 12.5 --duration 8 -o slice.jpg
```

### Step 5: 从 stdin 读取

```bash
cat track.mp3 | songsee - --format png -o out.png
```

## Visualization Types

Use `--viz` with comma-separated values:

| Type | Description |
|------|-------------|
| `spectrogram` | Standard frequency spectrogram |
| `mel` | Mel-scaled spectrogram |
| `chroma` | Pitch class distribution |
| `hpss` | Harmonic/percussive separation |
| `selfsim` | Self-similarity matrix |
| `loudness` | Loudness over time |
| `tempogram` | Tempo estimation |
| `mfcc` | Mel-frequency cepstral coefficients |
| `flux` | Spectral flux (onset detection) |

Multiple `--viz` types render as a grid in a single image.

## Common Flags

| Flag | Description |
|------|-------------|
| `--viz` | Visualization types (comma-separated) |
| `--style` | Color palette: `classic`, `magma`, `inferno`, `viridis`, `gray` |
| `--width` / `--height` | Output image dimensions |
| `--window` / `--hop` | FFT window and hop size |
| `--min-freq` / `--max-freq` | Frequency range filter |
| `--start` / `--duration` | Time slice of the audio |
| `--format` | Output format: `jpg` or `png` |
| `-o` | Output file path |

## 异常处理

| 场景 | 处理方式 |
|------|---------|
| 文件不存在 | 检查文件路径，使用 `ls` 确认文件存在 |
| 不支持的音频格式 | 安装 `ffmpeg`：`sudo apt install ffmpeg` 或 `brew install ffmpeg` |
| Go 未安装 | 按 Prerequisites 安装 Go 工具链 |
| songsee 未找到 | 运行 `go install github.com/steipete/songsee/cmd/songsee@latest` 重新安装 |
| 内存不足（大文件） | 使用 `--start`/`--duration` 缩小处理范围，或降低 `--width`/`--height` |
| 输出文件写入失败 | 检查磁盘空间和目标目录写权限 |
| 音频文件损坏 | 先用 `ffmpeg -i track.mp3` 验证文件完整性 |

## 注意事项（避坑）

- **格式支持**: WAV 和 MP3 原生解码；FLAC/OGG/AAC 等需要 `ffmpeg`
- **输出查看**: 生成的图片可用 `vision_analyze` 工具进行自动化音频分析
- **对比场景**: 对同一歌曲的不同版本（如原版 vs remix）使用相同参数生成，便于视觉对比
- **调试用途**: `hpss` 适合分析打击乐和旋律分离，`flux` 适合 onset 检测调试
