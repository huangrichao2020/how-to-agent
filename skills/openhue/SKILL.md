---
name: openhue
description: Control Philips Hue lights, rooms, and scenes via the OpenHue CLI. Turn lights on/off, adjust brightness, color, color temperature, and activate scenes.
category: smart-home
version: 1.2.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Smart-Home, Hue, Lights, IoT, Automation]
    homepage: https://www.openhue.io/cli
prerequisites:
  commands: [openhue]
---

# OpenHue CLI

Control Philips Hue lights and scenes via a Hue Bridge from the terminal.

## Prerequisites

```bash
# Linux（示例：安装预编译二进制）
curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue

# macOS（示例）
brew install openhue/cli/openhue-cli
```

Verify installation:
```bash
openhue --version
```

**注意：** First-time setup requires pressing the physical button on your Hue Bridge to authorize the CLI. The bridge must be on the same local network.

## 执行步骤

1. 确认 openhue CLI 已安装（`which openhue`）
2. 确认 Hue Bridge 在同一局域网且可达
3. 执行预检命令列出可用资源（灯、房间、场景）
4. 根据用户需求执行控制命令
5. 验证执行结果，处理可能的错误

## When to Use

- "Turn on/off the lights"
- "Dim the living room lights"
- "Set a scene" or "movie mode"
- Controlling specific Hue rooms, zones, or individual bulbs
- Adjusting brightness, color, or color temperature

## Pre-flight checks（示例）

```bash
# 1. 验证 CLI 已安装
which openhue || echo "openhue not found — install first"

# 2. 验证桥接器连接
openhue get light 2>&1 || echo "⚠️ Bridge unreachable — check network and IP"

# 3. 列出可用资源
openhue get light   # 灯
openhue get room    # 房间
openhue get scene   # 场景
```

## Common Commands（示例）

### Control Lights

```bash
# 示例：开关灯
openhue set light "Bedroom Lamp" --on
openhue set light "Bedroom Lamp" --off

# 示例：调节亮度 (0-100)
openhue set light "Bedroom Lamp" --on --brightness 50

# 示例：色温调节 (warm to cool: 153-500 mirek)
openhue set light "Bedroom Lamp" --on --temperature 300

# 示例：颜色设置（按名称或 hex）
openhue set light "Bedroom Lamp" --on --color red
openhue set light "Bedroom Lamp" --on --rgb "#FF5500"
```

### Control Rooms（示例）

```bash
# 关闭整个房间
openhue set room "Bedroom" --off

# 设置房间亮度
openhue set room "Bedroom" --on --brightness 30
```

### Scenes（示例）

```bash
openhue set scene "Relax" --room "Bedroom"
openhue set scene "Concentrate" --room "Office"
```

## Quick Presets（示例）

```bash
# 睡前模式（暖光低亮）
openhue set room "Bedroom" --on --brightness 20 --temperature 450

# 工作模式（冷光高亮）
openhue set room "Office" --on --brightness 100 --temperature 250

# 观影模式（微光）
openhue set room "Living Room" --on --brightness 10

# 全部关闭
openhue set room "Bedroom" --off
openhue set room "Office" --off
openhue set room "Living Room" --off
```

## 异常处理 / Error Handling

| 错误场景 | 原因 | 解决方案 |
|---------|------|---------|
| `openhue: command not found` | openhue 未安装 | 运行对应平台的安装命令 |
| `bridge not found` / connection timeout / 超时 | 桥接器离线或不在同一网络 | 检查桥接器电源；确认在同一 LAN；检查桥接器 IP |
| `link button not pressed` | CLI 未获得授权 | 30 秒内按下 Hue Bridge 上的物理按钮 |
| `light not found` | 灯名称错误或灯离线 | 运行 `openhue get light` 查看准确名称（注意大小写） |
| `room not found` | 房间名称不存在 | 运行 `openhue get room` 查看准确名称（区分大小写） |
| `scene not found` | 场景不适用于目标房间 | 运行 `openhue get scene` 列出可用场景 |
| 颜色命令被忽略 | 灯泡不支持彩色（仅白色） | 检查灯泡型号；颜色仅对彩色灯泡生效 |
| `unauthorized` / 授权失败 | 授权令牌过期 | 重新运行任意 openhue 命令并按下桥接器按钮重新授权 |
| 命令挂起 / 无响应 | 桥接器 IP 改变或网络问题 | 检查桥接器 IP；更新配置文件 |
| `Error: connection refused` | 桥接器完全不可达 | 检查网络连接；重启桥接器；确认 IP 地址正确 |

**兜底策略 / Fallback：**
- CLI 命令失败 → 重试一次（桥接器有时需要短暂重连）
- 网络不可达 → 延迟重试，或检查 Hue Bridge 是否断电
- 名称不匹配 → 先用 `openhue get light/room/scene` 列出准确名称
- 持续失败 → 回退到 Hue API（通过 curl 直接调用桥接器 REST API）

## 注意事项 / Pitfalls

1. **始终先列出资源再操作** — 使用 `openhue get light/room/scene` 确认名称准确
2. **名称区分大小写** — 必须使用列表中的准确名称（包括大小写）
3. **桥接器必须在同一局域网** — 不同网段无法通信
4. **首次使用需按物理按钮** — 这是 Hue 的安全机制，无法跳过
5. **颜色只对彩色灯泡生效** — 白色灯泡会静默忽略颜色参数
6. **测试时先操作单个灯泡** — 确认无误后再应用到整个房间
7. **禁止在生产环境中大规模频繁开关** — 可能影响灯泡寿命
8. **确认网络稳定后再执行自动化脚本** — 网络波动会导致命令超时失败
