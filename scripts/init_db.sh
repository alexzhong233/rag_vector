#!/bin/bash
# 启动PostgreSQL数据库

echo "Starting PostgreSQL with pgvector..."

# 检查Docker是否安装
if ! command -v docker &> /dev/null; then
    echo "Error: Docker is not installed"
    exit 1
fi

# 启动容器
docker-compose up -d

# 等待数据库就绪
echo "Waiting for database to be ready..."
sleep 5

# 连接到数据库并启用pgvector
docker exec -it rag_postgres psql -U postgres -d rag_db -c "CREATE EXTENSION IF NOT EXISTS vector;"

echo "Database is ready!"
echo "Connection string: postgresql://postgres:postgres@localhost:5432/rag_db"
