---
name: skill-quality-upgrade-pattern
description: "Use when upgrading existing Hermes skills to the new high-quality template structure. Trigger: 升级 skill / 优化 skill 质量 / 按新模板重构 skill. Do NOT trigger for creating new skills (use skill-design-template) or minor content edits."
version: 1.0.0
---

# Skill 质量升级模式

## 一句话版本

将现有平铺式 SKILL.md 升级为分层结构化模板。核心：提取反模式、编写决策树、拆分 references、添加检查清单。

## 如何使用本技能

1. **读取目标 skill**：用 `skill_view` 获取当前内容
2. **识别差距**：对比 native-feel-skill 结构（触发条件/反模式/分层参考/检查清单）
3. **创建目录结构**：`references/` + `checklists/`
4. **编写分层文件**：philosophy → API/patterns → pitfalls → decision-tree → ship-readiness
5. **重写主 SKILL.md**：引用配套文件，保留核心逻辑
6. **同步到 how-to-agent**：运行 `sync_skills_to_how_to_agent.py --push --skill <name>`

## 核心反模式（看到这些立刻停下）

- **"直接复制粘贴旧内容到新文件"** → 必须重新提炼，不能简单搬家
- **"一次性升级所有 229 个 skill"** → 先升级 3-5 个高频 skill 验证模板，再逐步推广
- **"不写反模式清单"** → 这是新模板的核心价值，必须至少 5 条
- **"不分层 references"** → 全部 dump 在一个文件里违背渐进式披露原则
- **"不更新版本号"** → 每次升级必须 bump version（minor 或 patch）
- **"升级后不同步到 how-to-agent"** → 必须推送到外部仓库留痕

## 标准升级步骤

### Step 1: 读取并分析
```python
skill_view(name="<skill-name>")
# 识别当前结构缺失：反模式？决策树？分层参考？
```

### Step 2: 创建目录
```bash
mkdir -p ~/.hermes/skills/<category>/<skill>/references
mkdir -p ~/.hermes/skills/<category>/<skill>/checklists
```

### Step 3: 编写 references
- `01-philosophy.md` — 核心原则 + 哲学
- `02-api-reference.md` 或 `02-patterns.md` — 技术细节
- `03-pitfalls.md` — 常见坑

### Step 4: 编写 checklists
- `decision-tree.md` — 适用性判断流程
- `ship-readiness.md` — 交付前检查

### Step 5: 重写 SKILL.md
- 保留 frontmatter（更新 version）
- 添加"一句话版本"
- 添加"如何使用本技能"（引用配套文件）
- 添加 5-6 条核心反模式
- 列出配套文件清单

### Step 6: 同步
```bash
python3 ~/hermes-agent/scripts/sync_skills_to_how_to_agent.py --push --skill <name>
```

## 已验证的升级案例

1. `a-stock-data` v4.0 → v4.1：增加数据源优先级矩阵 + 腾讯 API GBK 编码陷阱
2. `self-healing-browser-extractor` v1.2 → v1.3：增加自愈循环哲学 + Cookie 复用模式
3. `douyin-content-extraction` v2.1 → v2.2：增加反爬策略详解 + Vision API 失效处理
4. `wechat-article-extraction` v1.x → v2.0：增加 HTML 实体解码模式 + OG 标签提取
5. `a-stock-limit-up-tracker` v2.0 → v2.1：增加 reason 字段优先原则 + MX API 配额管理

## 配套工具

- 同步脚本：`~/hermes-agent/scripts/sync_skills_to_how_to_agent.py`
- 自动 cron：每 6 小时扫描变更并推送（job_id: `3a3c0ca1db0f`）
- 模板参考：`skill-design-template`