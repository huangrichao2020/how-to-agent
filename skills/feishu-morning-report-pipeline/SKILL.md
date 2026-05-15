---
name: feishu-morning-report-pipeline
description: 盘前热点早报自动化管线 - 从复盘盒子数据库读取消息面，去重后推送到飞书。解决微信文章硬编码链接和 lark-cli 命令不存在的问题。
tags: [cron, feishu, fupanhezi, automation]
---

# 盘前热点早报自动化管线

## 背景
旧方案依赖微信公众号文章链接（硬编码 URL），存在两个致命问题：
1. **链接失效**：公众号每天更新，旧链接无法获取最新内容
2. **推送失败**：`lark-cli message send` 命令不存在，导致 cron 执行报错

新方案改用**复盘盒子 SQLite 数据库**作为数据源，通过 `push_feishu.py` 推送，实现稳定、结构化的早报生成。

## 核心组件

### 1. 数据脚本：`/root/hermes-agent/tools/fupan_data/morning_report.py`
- **数据源**：`~/.hermes/data/fupanhezi/fupanhezi.db`（SQLite）
- **逻辑**：
  1. 查询最新交易日 (`zt_data` 表)
  2. 提取该日消息面 (`news_data` 表)
  3. 格式化 TOP 15 热点（标题 + 标签）
  4. MD5 去重（对比 `~/.hermes/cache/morning_report_last.md5`）
  5. 调用 `push_feishu.py` 推送
- **频控**：无（本地数据库读取，秒级响应）

### 2. 推送脚本：`/root/hermes-agent/scripts/stock_monitor/push_feishu.py`
- **协议**：Feishu Open API (`POST /open-apis/im/v1/messages`)
- **认证**：从 `~/.hermes/.env` 读取 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`
- **目标**：`FEISHU_STOCK_CHAT_ID` (Home Channel)

### 3. Cron Job：`盘前热点早报-复盘盒子` (ID: `4d43756fa78f`)
- **Schedule**：`20 8 * * 1-5`（每交易日 08:20）
- **Prompt**：直接运行 `python3 /root/hermes-agent/tools/fupan_data/morning_report.py`
- **Delivery**：`feishu`

## 常见陷阱

### 1. lark-cli 命令不存在
- **错误**：`lark-cli message send` 是无效命令
- **正确**：使用 `lark-cli api POST /open-apis/im/v1/messages` 或直接调用 `push_feishu.py`
- **原因**：lark-cli 的 schema 中 `im.messages` 只有 `delete`, `forward` 等方法，没有 `create`

### 2. Cron Prompt 缓存问题
- **现象**：更新了 jobs.json 中的 prompt，但 cron 运行时仍执行旧逻辑
- **根因**：Hermes cron 系统在 session 启动时注入 prompt，可能存在缓存或版本不一致
- **解决**：**删除旧 job，创建新 job**，不要尝试 update prompt

### 3. 消息面数据结构差异
- **现象**：`news_data` 表中的 `raw_data` 可能是 dict 或 list
- **处理**：
  ```python
  data = json.loads(row[0])
  items = data.get("data", [])
  if isinstance(data, dict):
      items = data.get("data", data)
  if isinstance(items, dict):
      items = items.get("data", [])
  ```

## 验证步骤
1. 手动运行脚本：`python3 /root/hermes-agent/tools/fupan_data/morning_report.py`
2. 检查输出：应显示"最新交易日"、"消息面数量"、"✅ 推送成功"
3. 检查飞书：收到格式正确的早报消息
4. 检查缓存：`~/.hermes/cache/morning_report_last.md5` 已更新

## 扩展建议
- 如需增加"市场风格判断"模块，可在脚本中增加指数行情查询（腾讯 API）
- 如需推送 Markdown 富文本，修改 `push_feishu.py` 支持 `post` 类型消息