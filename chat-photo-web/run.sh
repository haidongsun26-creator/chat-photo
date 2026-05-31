#!/bin/bash
# chat-photo web 启动脚本（零第三方依赖，仅需 python3）
# 用法：  ./run.sh        然后浏览器开 http://127.0.0.1:8000
set -e
cd "$(dirname "$0")"

# 载入 .env（若存在）
if [ -f .env ]; then
  set -a; . ./.env; set +a
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "⚠️  未检测到 ANTHROPIC_API_KEY —— 看图会失败。"
  echo "   请: cp .env.example .env  然后在 .env 里填 key，再重跑 ./run.sh"
fi

exec python3 server/app.py
