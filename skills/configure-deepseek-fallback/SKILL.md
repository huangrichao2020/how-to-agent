---
name: configure-deepseek-fallback
title: 配置 DeepSeek 作为百炼 429 错误的后备提供商
description: 在 ~/.hermes/config.yaml 中添加 fallback_providers，确保在百炼 CodingPlan 返回 429 限流时自动切换到 DeepSeek (deepseek-v4-flash) 而不走 OpenRouter。
---

## 步骤
1. **查看当前配置**
   ```bash
   cat ~/.hermes/config.yaml
   ```
   确认 `fallback_providers` 和 `fallback_model` 两个字段的状态。

2. **先移除遗留的 `fallback_model`（关键！）**
   ```bash
   grep -A2 '^fallback_model:' ~/.hermes/config.yaml
   ```
   - 如果 `fallback_model` 存在且指向 `openrouter`，它**会优先于** `fallback_providers` 使用，导致实际回退仍走 OpenRouter。
   - **必须彻底删除或注释掉** `fallback_model` 整段，只留 `fallback_providers`。
   - 使用 `patch` 删除：
     ```
     patch --mode replace \
       --old "fallback_model:\n  provider: openrouter\n  model: openrouter/auto" \
       --new "" \
       ~/.hermes/config.yaml
     ```
   - 或者改成空对象 `fallback_model: {}`。

3. **使用 `patch` 添加 DeepSeek 到 fallback_providers**
   ```bash
   patch --mode replace \
     --old "fallback_providers: []" \
     --new "fallback_providers:\n  - provider: deepseek\n    model: deepseek-v4-flash\n    base_url: https://api.deepseek.com/v1\n    request_timeout_seconds: 120" \
     ~/.hermes/config.yaml
   ```
   - 如果已有其他 fallback 条目，手动将上述块合并到列表中，保持 YAML 缩进。

4. **验证修改**
   ```bash
   grep -A3 -E '(fallback_providers|fallback_model)' ~/.hermes/config.yaml
   ```
   确认：
   - `fallback_model` 不存在或为空（`fallback_model: {}`）
   - `fallback_providers` 下包含正确的 deepseek 条目

5. **确保 DeepSeek API Key 已配置**
   ```bash
   grep DEEPSEEK_API_KEY ~/.hermes/.env || echo "# 添加 DeepSeek API Key" >> ~/.hermes/.env
   ```
   将 `DEEPSEEK_API_KEY=your_key_here` 写入 `.env`（如果尚未存在）。

6. **重启或重新加载 Hermes Agent**（视部署方式而定）
   ```bash
   hermes restart   # 若在本地运行
   # 或者重新开启会话，让新配置生效
   ```

## 常见问题 / 注意事项

### ⚠️ fallback_providers 可能不自动触发（关键发现）
配置 `fallback_providers` **不代表 429 限流时会自动切换**。实践中发现：
- 百炼返回 429 后，系统仍会在同一 provider 上重试 3 次
- 3 次都失败后抛 `Empty response from model`，**不会自动切到 fallback**
- `fallback_providers` 可能只在其他特定场景下生效（如连接超时、DNS 失败）

**可靠的工作流（遇到 429 时）**：

1. **确认是 429**：
   ```bash
   journalctl -u hermes-gateway --since "5 min ago" | grep -i "429\|quota\|throttling\|RateLimit"
   ```

2. **手动切换默认 provider 到 deepseek**：
   ```bash
   sed -i 's/^  provider: alibaba-coding-plan$/  provider: deepseek/' ~/.hermes/config.yaml
   sed -i 's/^  default: qwen3.6-plus$/  default: deepseek-v4-flash/' ~/.hermes/config.yaml
   ```

3. **重启 Gateway**：
   ```bash
   hermes gateway restart
   ```

4. **百炼配额次日 0 点刷新**，届时可切回：
   ```bash
   sed -i 's/^  provider: deepseek$/  provider: alibaba-coding-plan/' ~/.hermes/config.yaml
   sed -i 's/^  default: deepseek-v4-flash$/  default: qwen3.6-plus/' ~/.hermes/config.yaml
   ```

### 其他注意事项
- **YAML 缩进**：列表项必须使用两个空格缩进，错误的缩进会导致配置加载失败。
- **已有 fallback 列表**：不要直接覆盖整个列表，改为在现有列表后追加新项，防止丢失其他后备提供商。
- **DeepSeek 密钥**：密钥必须在 `~/.hermes/.env` 中，以 `DEEPSEEK_API_KEY` 命名；否则调用会报未授权错误。
- **生效时机**：配置文件在 Agent 启动时读取，运行中的实例需要重启才能识别新 fallback。

## 参考
- `~/.hermes/config.yaml` – Hermes 主配置文件。
- Hermes 文档中关于 `fallback_providers` 的说明。
