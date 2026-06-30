---
name: agent-skill-creator_Skill技能自动构建器
description: 当 agent 需要创建、更新、管理、验证或淘汰自己的可复用技能时使用。覆盖触发词设计、目录结构、渐进加载、运行时索引、技能使用习惯，以及 GA/Hermes 风格 agent 的任务后技能维护。
---

# Agent 技能创建器

当一次对话产生了可复用能力，agent 应该把它变成 durable skill，而不是只留在
聊天记录里。

## 核心姿态

Skill 不是 prompt 堆砌。Skill 是可复用的操作知识：有清楚触发条件、简洁流程、
可选 reference/script，并且验证过运行时能找到、能使用。

```text
重复需求 -> 可复用流程 -> skill 包 -> 索引验证 -> 真实使用 -> 持续维护
```

更准确地说：

```text
prompt 是一次性会话指令。
Skill 是跨会话、按需发现、可执行、可版本管理的能力包。
```

Skill 的价值不在 Markdown 正文像不像 prompt，而在三件事：

- 渐进披露：常驻只保留 `name + description`，触发后才读正文，长资料按需读。
- 脚本确定性：格式敏感、可重复、可校验的步骤交给 `scripts/`。
- 长期资产：skill 能被 git 管理、review、安装、索引、复用和淘汰。

## 什么时候创建 skill

满足任意一条就应该创建或更新 skill：

- 同一工作流以后大概率还会用；
- 涉及脆弱外部系统、API、工具或文件格式；
- agent 反复写同一种 helper script 或 checklist；
- 用户明确说要学会、记住、以后使用这个能力；
- 这次经验是操作性的，不只是事实；
- 已经在真实任务里验证过，应当沉淀为长期能力。

不要为了单次事实、私密原始日志、密钥，或很小的记忆点创建 skill。

## Skill Admission Gate

创建 Skill 前先问：

1. 这个流程会重复吗？
2. 它是否需要跨会话、跨 agent 或团队共享？
3. 它是否包含必须稳定执行的步骤？
4. 它是否能用脚本降低不确定性？
5. 它是否比一段 prompt 更能降低上下文成本？

如果大多是否，写 prompt、memory 或普通文档即可。

## Skill 结构

推荐目录：

```text
skill-name/
├── SKILL_技能说明与使用指南.md
├── SKILL_技能说明中文版.md
├── references/
│   └── source-map.md
├── scripts/
│   └── optional-helper.py
└── assets/
    └── optional-template-or-media
```

GA 当前扁平运行时索引还需要一个精简版：

```text
skills/<domain>/<skill-name>.md
```

M1 Hermes 应同时安装到：

```text
~/Desktop/hermes-agent/skills/<skill-name>/
~/.hermes/skills/<skill-name>/
```

## 触发描述设计

frontmatter 里的 `description` 是触发器。它要回答：

- 这个 skill 做什么；
- 什么时候使用；
- 用户可能怎么说；
- 不应和什么混淆。

正文保持简洁。长资料放进 `references/`，并写清什么时候读取。

description 写得太宽会误触发，太窄会召回失败。它不是营销介绍，而是运行时发现机制。

## 渐进披露设计

Skill 按三层组织：

```text
L1 metadata: name + description
  只用于发现和触发。

L2 SKILL_技能说明与使用指南.md / SKILL_技能说明中文版.md
  只放核心流程、禁忌、输出和验证。

L3 references / scripts / assets
  长资料、确定性脚本、模板、示例，用到哪个读哪个。
```

主文件不要变成长 prompt。判断标准：如果某段内容不是每次触发都要看，就拆出去。

## 脚本确定性

这些内容优先放进 `scripts/`：

- 排序、聚合、校验、格式转换。
- 文档、表格、PDF、图片、视频等文件结构操作。
- API 参数校验、批量请求、重试和分页。
- 输出大小、文件完整性、schema、lint、测试。
- 能用代码一次算准的事。

模型负责判断和取舍；脚本负责确定性和验证。脚本源代码不需要整段进入上下文，脚本输出才进入上下文。

## 创建流程

1. **提炼能力。**
   用一句话写清可复用动作。如果只是事实，放进 memory，不要做 skill。

2. **命名 skill。**
   用短的 kebab-case 名称，描述任务本身，不要只写来源文章名。

3. **写触发条件。**
   `description` 要足够自然，能触发；也要足够窄，不乱加载。

4. **写核心流程。**
   优先包含：
   - 核心立场；
   - 5-8 步工作流；
   - 反粗糙规则；
   - 输出约定；
   - 验证步骤。

5. **使用渐进加载。**
   `SKILL_技能说明与使用指南.md` 保持短。长 source map、API、示例、模板放进
   `references/`、`scripts/`、`assets/`。

6. **安装进运行时。**
   能力库里放 portable skill，agent 实际索引目录里放运行时精简版。

7. **重建或验证索引。**
   确认运行时能看见：
   - GA：运行 `skill_registry.prompt_summary(...)` 或重建
     `skills/index-cache/skills_index.json`。
   - Hermes：运行本地 skill list/view 命令，或检查 skill index。

8. **真实使用一次。**
   skill 必须指导过真实任务或 smoke prompt，才算活了。

9. **持续维护。**
   实战后只把验证过的东西写回 skill。删除过期警告，合并重复 skill，
   归档不用的 skill。

## 管理规则

- 优先改进已有 skill，不要制造近义重复。
- skill 要高信号，不能把 skills 目录变成杂物间。
- skill 应该增强行动能力，不要制造审批仪式。
- skill 过长时拆 reference，不要堆进主文件。
- 很少使用或过于领域化的 skill，应离开核心每日 skill 集。
- 不要把密钥、原始私密日志、凭证、token 写进 skill。
- 不要安装不可信 skill；带脚本的 skill 必须审查读写路径、外部下载、权限和数据外传。
- 不要把本来一句话能解决的问题硬封装成 skill。

## 输出约定

创建或更新 skill 时汇报：

1. skill 名称和触发条件；
2. 改了哪些文件；
3. 它以后怎么被使用；
4. 做了什么验证；
5. GA/Hermes 运行时索引是否已更新。
