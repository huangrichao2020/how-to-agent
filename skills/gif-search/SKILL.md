---
name: gif-search
description: Search and download GIFs from Tenor using curl. No dependencies beyond curl and jq. Useful for finding reaction GIFs, creating visual content, and sending GIFs in chat.
version: 1.2.0
author: Hermes Agent
license: MIT
prerequisites:
  env_vars: [TENOR_API_KEY]
  commands: [curl, jq]
metadata:
  hermes:
    tags: [GIF, Media, Search, Tenor, API]
    category: media
---

# GIF Search (Tenor API)

Search and download GIFs directly via the Tenor API using curl. No extra tools needed.

## 触发条件

当用户需要以下场景时触发此 Skill：
- 搜索特定主题的 GIF（表情包、反应图等）
- 获取 GIF 的下载链接或直接下载
- 在聊天/Markdown 中嵌入 GIF

## Setup

Set your Tenor API key in your environment (add to `~/.hermes/.env`):

```bash
TENOR_API_KEY=your_api_key_here
```

Get a free API key at https://developers.google.com/tenor/guides/quickstart — the Google Cloud Console Tenor API key is free and has generous rate limits.

## Prerequisites

- `curl` and `jq` (both standard on macOS/Linux)
- `TENOR_API_KEY` environment variable set

## 工作流程

### Step 1: 搜索 GIF

```bash
# 搜索并获取 GIF URL 列表
curl -sf "https://tenor.googleapis.com/v2/search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('thumbs up'))")&limit=5&key=$TENOR_API_KEY" | jq -r '.results[].media_formats.gif.url'
```

### Step 2: 获取预览/小尺寸版本（适合聊天发送）

```bash
curl -sf "https://tenor.googleapis.com/v2/search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('nice work'))")&limit=3&key=$TENOR_API_KEY" | jq -r '.results[].media_formats.tinygif.url'
```

### Step 3: 下载 GIF

```bash
# 搜索并下载 top result
URL=$(curl -sf "https://tenor.googleapis.com/v2/search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('celebration'))")&limit=1&key=$TENOR_API_KEY" | jq -r '.results[0].media_formats.gif.url')
if [ -n "$URL" ] && [ "$URL" != "null" ]; then
  curl -sL "$URL" -o celebration.gif
  echo "Downloaded: celebration.gif"
else
  echo "Error: No results found or API returned empty"
fi
```

### Step 4: 获取完整元数据

```bash
curl -sf "https://tenor.googleapis.com/v2/search?q=$(python3 -c "import urllib.parse; print(urllib.parse.quote('cat'))")&limit=3&key=$TENOR_API_KEY" | jq '.results[] | {title: .title, url: .media_formats.gif.url, preview: .media_formats.tinygif.url, dimensions: .media_formats.gif.dims}'
```

## API Parameters

| Parameter | Description |
|-----------|-------------|
| `q` | Search query (URL-encode spaces as `%20` or `+`) |
| `limit` | Max results (1-50, default 20) |
| `key` | API key (from `$TENOR_API_KEY` env var) |
| `media_filter` | Filter formats: `gif`, `tinygif`, `mp4`, `tinymp4`, `webm` |
| `contentfilter` | Safety: `off`, `low`, `medium`, `high` |
| `locale` | Language: `en_US`, `es`, `fr`, etc. |

## Available Media Formats

Each result has multiple formats under `.media_formats`:

| Format | Use case |
|--------|----------|
| `gif` | Full quality GIF |
| `tinygif` | Small preview GIF (ideal for chat) |
| `mp4` | Video version (smaller file size) |
| `tinymp4` | Small preview video |
| `webm` | WebM video |
| `nanogif` | Tiny thumbnail |

## 异常处理

| 场景 | 处理方式 |
|------|---------|
| API 返回空结果 | 检查拼写，尝试更宽泛的关键词，或调整 `contentfilter` |
| HTTP 429 (Rate Limited) | 等待后重试，或减少 `limit` 值 |
| HTTP 401/403 (Auth Error) | 检查 `$TENOR_API_KEY` 是否有效，确认 API 已启用 |
| curl 超时/网络错误 | 使用 `curl -sf --max-time 10` 设置超时，失败时 fallback 到备用搜索词 |
| jq 解析失败 | 检查 API 响应是否为有效 JSON，确认 `.results` 字段存在 |
| 下载失败 | 检查 URL 是否可达，确认网络连通性 |

## 注意事项（避坑）

- **URL 编码**: 查询参数中的空格和特殊字符必须 URL 编码，推荐使用 `python3 -c "import urllib.parse; print(urllib.parse.quote('query here'))"`
- **API Key 安全**: 不要硬编码 key，始终从环境变量读取
- **文件过大**: 聊天场景优先使用 `tinygif`，完整 `gif` 可能超过消息大小限制
- **Markdown 嵌入**: GIF URL 可直接用于 `![alt](url)` 语法
- **Rate Limit**: Tenor API 有速率限制，批量搜索时加适当间隔
