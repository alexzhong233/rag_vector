#!/bin/bash

echo "🚀 启动 RAG 管理系统"

# 检查 Docker 是否安装
if ! command -v docker &> /dev/null; then
    echo "❌ Docker 未安装，请先安装 Docker"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
    exit 1
fi

# 检查 OPENAI_API_KEY 是否设置
if [ -z "$OPENAI_API_KEY" ]; then
    echo "⚠️  OPENAI_API_KEY 未设置"
    echo "请设置环境变量: export OPENAI_API_KEY=your-api-key"
    echo "或创建 .env 文件"
    echo ""
    
    # 尝试从 .env 文件读取
    if [ -f .env ]; then
        echo "📄 检测到 .env 文件，正在加载..."
        export $(grep -v '^#' .env | xargs)
    else
        echo "❌ 请先设置 OPENAI_API_KEY"
        exit 1
    fi
fi

echo "✅ OpenAI API Key 已配置"
echo ""

# 创建必要的目录
mkdir -p uploads

# 启动服务
echo "📦 正在启动所有服务..."
if command -v docker-compose &> /dev/null; then
    docker-compose -f docker-compose-full.yml up -d --build
else
    docker compose -f docker-compose-full.yml up -d --build
fi

echo ""
echo "✅ 服务启动完成！"
echo ""
echo "🌐 访问地址："
echo "  前端界面: http://localhost:5173"
echo "  后端API:  http://localhost:8080"
echo "  数据库:   localhost:5432"
echo ""
echo "📋 查看日志: docker-compose -f docker-compose-full.yml logs -f"
echo "⏹️  停止服务: docker-compose -f docker-compose-full.yml down"
