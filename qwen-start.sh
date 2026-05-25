#!/bin/bash
# qwen-start.sh - 在 how-to-agent 项目下启动 qwen CLI
# 用法: ./qwen-start.sh [参数]

set -e

# 底座项目目录
HOW_TO_AGENT="$HOME/Desktop/how-to-agent"

# 确保目录存在
mkdir -p "$HOW_TO_AGENT/.qwen"

# 设置环境变量
export BAILIAN_CODING_PLAN_API_KEY="sk-sp-005821af43554fd39e6e4cd08766ff30"

# 切换到 how-to-agent 目录
cd "$HOW_TO_AGENT"

# 启动 qwen
if [ $# -eq 0 ]; then
  # 无参数时进入交互模式
  qwen --auth-type openai \
       --openai-api-key "$BAILIAN_CODING_PLAN_API_KEY" \
       --openai-base-url "https://coding.dashscope.aliyuncs.com/v1" \
       --model "qwen3.6-plus"
else
  # 有参数时执行 prompt 后退出
  qwen --auth-type openai \
       --openai-api-key "$BAILIAN_CODING_PLAN_API_KEY" \
       --openai-base-url "https://coding.dashscope.aliyuncs.com/v1" \
       --model "qwen3.6-plus" \
       "$@"
fi
