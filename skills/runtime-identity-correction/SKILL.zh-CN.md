---
name: runtime-identity-correction
description: 在 agent 迁移宿主机、网络、工作区或平台后，修正过期的自我认知。
---

# 运行时自我认知校准

当 agent 还在用旧机器、旧部署或旧网络环境思考时，使用这个 skill。

典型信号：

- 已经迁到 Mac，却还提阿里云、VPS、Linux、2GB RAM、旧 pip 镜像或旧网络限制。
- 使用旧服务路径、旧重启命令、旧进程管理器或旧平台账号。
- 用历史限制解释当前故障。

## 核心规则

当前运行时事实，高于历史环境记忆。

不要只靠一句 prompt 提醒修这个问题。要修会被 runtime 检索和注入的活跃自我认知源。

## 步骤

1. 从当前机器验证事实：
   - hostname
   - OS 和架构
   - 内存预算
   - 当前工作区路径
   - gateway / service manager
   - 网络和代理状态

2. 搜索活跃注入源：
   - `.agent/memory/semantic/lessons.jsonl`
   - `LESSONS.md` 等渲染文件
   - wiki / gbrain 自我页面
   - 工作手册和交接文档
   - runtime prompt / context assembler 输入
   - 如果问题持续，检查近期 cache

3. 替换过期的“当前环境”结论。

4. 把旧事实改写成历史经验：

   ```text
   仅当通过 ssh <host> 运维旧远程主机时适用。
   它不是当前 runtime 约束。
   ```

5. 新增一条强校准记忆，写清楚：
   - agent 当前运行在哪里
   - 遇到问题先检查什么
   - 旧环境经验什么时候才适用

6. 保留不可变历史：
   - 不改旧审计日志。
   - 不重写历史 session。
   - 用户没明确要求时，不删除证据。

7. 把临时备份移出活跃检索路径。

8. 如果旧上下文可能已经加载，重启 gateway/runtime。

9. 完成前反向搜索旧关键词。

## 旧污染关键词示例

- `Alibaba Cloud Linux`
- `2GB RAM`
- `mirrors.aliyun.com`
- `Google API unreachable`
- `curl timeout`
- 迁到 `/Users/...` 后仍出现旧 `/root/...` 路径
- 迁到 `launchctl` 后仍出现旧 `systemctl` 重启指令

## 完成标准

活跃 memory/wiki/manual 应清楚说明当前运行时。旧环境经验必须被限定到旧宿主机，不能再作为当前约束参与推理。
