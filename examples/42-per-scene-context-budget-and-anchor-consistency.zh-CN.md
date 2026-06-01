# 按场景裁剪上下文 + 锚点一致性校验

2026-06-01，Hermes 和 GenericAgent 在同一天内独立演化了四条可复用架构模式。这些不是理论设计，而是两个 agent 在真实运行中被 prompt 膨胀、状态漂移和响应延迟逼出来的解决方案。

## 为什么重要

agent 运行时最隐蔽的敌人不是 bugs，而是**逐渐膨胀的 system prompt**。每个新功能加一段规则，每段规则加几个触发词，几个月后 agent 每轮都在读 15,000+ tokens 的"说明书"，但其中 80% 跟当前任务无关。

同一天的对话里，道友指出 Hermes "响应太慢了"，小GA 发现自己的 token 分布里 memory recall block 吃掉了大头。两个 agent 独立走到了同一个结论：**按场景裁剪上下文，而不是全量注入。**

## 模式 1：按场景注入上下文（Per-Scene Context Budget）

### 核心洞察

```text
不做：把全部 tools / memory surfaces / cognitive frameworks 塞进每轮 prompt
要做：识别当前场景 → 只注入该场景需要的上下文 → 保持 core 兜底
```

### 三层裁剪：工具 / 记忆 / 认知

| 层 | 全量注入（旧） | 按场景注入（新） | token 节省 |
|---|---|---|---|
| **工具 Schema** | 全部 tools 描述注入 | CORE 14 个常驻，其余按关键词触发场景组注入 | 6-8K/turn |
| **记忆取用** | MemoryHub 7 个存储面全量注入 | coding 场景取 3 面，chat 取 2 面，stock 取 3 面 | 3-5K/turn |
| **认知采集框架** | L0-L5 分层 + 经验包四投影 + 认知闭环常驻 | 只在消息触发了认知关键词时才注入完整框架，其余走轻量模式 | 2.5K/turn |

### 实现骨架

```python
# 工具裁剪：CORE 常驻 + 场景触发组
CORE_TOOLS = {"terminal", "read_file", "search_files", "patch", ...}  # 14 个

GROUPS = {
    "browser": {"browser_navigate", "browser_snapshot", ...},
    "feishu": {"feishu_doc_create", "feishu_msg_send", ...},
    "stock": {"stock_quote", "ztb_track", ...},
    # ...
}

TRIGGERS = {
    "browser": ["网页", "浏览器", "打开链接", "web", "browser", "爬取"],
    "stock": ["股票", "涨停", "A股", "行情", "复盘", "盘前"],
    # ...
}

def select_tools(user_message: str) -> set[str]:
    selected = set(CORE_TOOLS)
    for group_name, keywords in TRIGGERS.items():
        if any(kw in user_message for kw in keywords):
            selected |= GROUPS[group_name]
    return selected
```

### 关键约束

- **CORE 永远在场**：即使场景分类失败，基础工具不丢，agent 不会报 unknown tool
- **用 min_tools 兜底**：如果匹配到的工具太少，补充到最小工具数（如 18 个）
- **描述压缩**：非 CORE 工具的 description 压缩到 120-180 字符
- **场景切换自动释放**：用户从"查股票"切换到"改代码"时，前一轮的 stock tools 自动释放

### 场景映射表（Hermes 实战数据）

| 场景 | 触发词 | MemoryHub 面数 | Tool Groups | 典型 token |
|---|---|---|---|---|
| coding | import/def/git/error/Traceback | 3 (episode+continuity+runtime_ledger) | core + dev + git | ~4K |
| chat | 闲聊/问候/感受 | 2 (channel+session_history) | core + feishu | ~2K |
| stock | 股票/涨停/A股/行情 | 3 (episode+cognition_store+user_state) | core + stock + data | ~5K |
| memory | 记忆/认知/知识/L5/因果 | 5 (全量+cognition_store+feedback) | core + memory_tools | ~6K |

## 模式 2：L1↔L2 锚点一致性校验

### 问题

agent 的 system prompt 每轮注入运行时状态（"当前项目是 info-hub""我在筑基 1 层""模型是 deepseek-v4-pro"），但这些注入值可能跟实际行为不匹配。比如：

- 注入说"项目是 info-hub"，但 tool calls 指向 hermes-agent 源码
- 注入说"模型是 deepseek"，但实际请求走了 mimo
- 注入说"筑基 1 层"，但 state.json 已经被 cron 更新到筑基 2 层

这些漂移如果不检测，会导致 agent 基于错误的前提做决策——记忆归档到错误项目、dream 复盘用错数据、回答时的自我认知完全离线。

### 解决方案

```text
注入日志（每次 turn）→ dream 夜间分析 → 一致性报告 → 下次 prompt 注入修正偏置
```

**第 1 步：注入日志落盘**（gateway/session.py）

每轮 `_build_runtime_state_section()` 返回前，写一行 JSON：

```json
{
  "ts": "2026-06-01T18:52:00",
  "cwd": "/Users/tingchi/hermes/hermes-agent",
  "repo": "hermes-agent",
  "cultivation": "筑基1层",
  "model": "deepseek-v4-pro",
  "platforms": ["feishu", "weixin"]
}
```

存储到 `~/.hermes/logs/anchor_drift/YYYY-MM-DD.jsonl`

**第 2 步：dream 夜间比对**（cognitive_dream.py）

`check_anchor_consistency(target_day)` 遍历注入日志 + runtime_ledger（实际 tool calls），逐锚点比对：

- **Level 1 事实校准**：cwd/repo 不匹配率 >60% → 标红
- **Level 2 多字段漂移**：多个锚点同时不匹配 → 升级严重度
- 输出 `consistency_YYYY-MM-DD.json`

**第 3 步：消费端注入**（GA 侧 anchor_consistency_consumer.py）

`format_for_prompt()` 将漂移结果转为轻量提示，注入下一轮 system prompt。不逐轮注入完整报告，只注入"当前已知漂移"的摘要。

### 为什么这是通用模式

任何有运行时状态感知的 agent 都会面临这个漂移问题。注入日志 → 夜间比对 → 轻量修正，这套流程不依赖特定 agent 架构：

- CLI agent：注入日志写文件，夜间脚本扫描
- Web agent：注入日志写 SQLite，cron job 分析
- Multi-agent：每个 agent 独立注入日志，共享一致性报告

## 模式 3：运行时状态自动注入

### 问题

agent 每轮都要回答"我是什么境界""我在哪个项目""现在几点"——如果不注入，就要反复读文件/调工具，浪费 token 和时间。

### 方案

gateway 层在构建 system prompt 时，实时读取并注入四块锚点：

```python
def _build_runtime_state_section(session_ctx: dict) -> str:
    now = datetime.now()
    return f"""
    - Time: {now.strftime('%Y-%m-%d %a %H:%M')}
    - Platform: {session_ctx.get('platform')}, Chat: {session_ctx.get('chat_name')}
    - Cultivation: {get_cultivation_from_state()}
    - Model: {get_active_model_from_config()}
    - Repo: {get_git_repo_name()}, CWD: {os.getcwd()}
    """
```

**核心原则：每轮重建，不缓存。** 生命周期只有一次 turn——不落盘、不跨轮复用、不依赖 memory 工具到达。这样即使 memory 注入失败，关键数据仍在 system prompt 中。

**跟 GA "文件为底 + 补丁"方案的对比：**

| | 每轮重建（Hermes） | 文件为底 + 补丁（GA） |
|---|---|---|
| 优点 | 永远是完整最新快照 | 不会意外覆盖 hot_context 里的其他事实 |
| 缺点 | 依赖实时文件读取的性能 | 需要管理文件状态和补丁冲突 |
| 适用场景 | 状态变化频繁、数据量小 | 状态变化少、需要保护其他上下文 |

## 模式 4：按任务复杂度路由模型

### 问题

所有消息用同一个模型——闲聊和改架构都走 deepseek-v4-pro，token 成本高、响应慢。

### 方案

```python
def classify_task_complexity(message: str) -> str:
    """简单的启发式分类，不调 LLM"""
    # 代码信号 → complex
    if any(kw in message for kw in ["```", "Traceback", "Error", "import", "def ", "class ", "git ", "pip "]):
        return "complex"
    # 架构信号 → complex  
    if any(kw in message for kw in ["架构", "重构", "设计", "迁移", "architecture"]):
        return "complex"
    # 股票信号 → complex
    if any(kw in message for kw in ["涨停", "盘前", "复盘", "选股", "交易策略"]):
        return "complex"
    return "lightweight"
```

- complex → deepseek-v4-pro / claude-sonnet
- lightweight → mimo-v2.5 / deepseek-v4-flash（便宜快）

**关键约束：不是文本分类器，是启发式筛选。** 宁可用便宜模型多跑一轮，也不要在分类阶段再调一次 LLM。分类失败的代价是偶尔用便宜模型回答复杂问题，但 CORE tools 始终在场，不会造成功能缺失。

## 落地证据

| 模式 | Hermes commit | GA 对应实现 |
|---|---|---|
| 按场景工具裁剪 | `bb55583` feat: tool schema budget | `GA_TOOL_SCHEMA_MODE` / `GA_TOOL_SCHEMA_EXTRA` |
| 按场景记忆裁剪 | `d9e3ef2` fix(memory_hub): per-scene surface budget | `cognitive_retrieval.py` per-face token budget |
| 认知采集分级注入 | `a4497e3` perf(cognitive_capture): tiered injection | — |
| 锚点一致性校验 | `fd88b8d` feat: anchor consistency check | `anchor_consistency_consumer.py` |
| 运行时状态注入 | `27b77ac` / `fa1982b` / `92f6145` | hot/cold memory split + frame_id |
| 复杂度路由模型 | `6415edf` feat: task-complexity model routing | — |

## 如何使用

1. **先裁剪工具**：把 tools 分组（CORE + 场景组），加触发词映射。这一步 token 节省最大，实现最简单。
2. **再裁剪记忆**：MemoryHub / recall 系统按场景只注入相关存储面。
3. **加注入日志**：在 prompt 构建函数返回前写一行 JSON。不需要一致性分析就能先积累数据。
4. **等数据后做一致性检查**：跑一周注入日志后，再写 dream 比对逻辑。数据不够时比对无意义。
5. **最后做模型路由**：启发式分类 + cheap/expensive 模型分派。这是锦上添花，不要影响前四步的主链路。

## 核心心法

```text
agent 优化不是加功能，是砍掉不该出现在当前场景的东西。
每一次"以防万一"的注入，都是未来响应延迟的债。
先让 agent 跑得快，再让它跑得准。
```
