#!/bin/bash

echo "⏹️  停止 RAG 管理系统"

if command -v docker-compose &> /dev/null; then
    docker-compose -f docker-compose-full.yml down
else
    docker compose -f docker-compose-full.yml down
fi

echo "✅ 服务已停止"
