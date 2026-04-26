# RAG管理系统

一个完整的文档管理和智能问答平台，支持文档导入、自动切片、向量化存储和语义检索功能。

## 技术栈

### 前端
- Vue 3 + TypeScript + Vite
- TailwindCSS
- Pinia (状态管理)
- Vue Router (路由)
- Lucide Vue (图标)

### 后端
- Java 17 + Spring Boot 3.2
- Spring Data JPA
- PostgreSQL + pgvector
- LangChain4j (LLM集成)
- Apache PDFBox (文档处理)

## 项目结构

```
rag_vector/
├── frontend/                 # Vue3前端项目
│   ├── src/
│   │   ├── components/      # 组件
│   │   ├── views/          # 页面
│   │   ├── router/         # 路由
│   │   ├── stores/         # 状态管理
│   │   └── api/            # API封装
│   └── Dockerfile.frontend
├── src/main/java/com/rag/  # Java后端项目
│   ├── controller/         # REST控制器
│   ├── service/            # 业务服务
│   ├── repository/         # 数据访问
│   ├── entity/             # 实体类
│   └── config/             # 配置
├── docker-compose-full.yml # 完整Docker编排
├── Dockerfile.backend      # 后端Dockerfile
└── README_FULL.md          # 本文档
```

## 快速开始

### 前置要求
- Docker 和 Docker Compose
- OpenAI API Key

### 方式一：使用Docker Compose (推荐)

1. 设置环境变量
```bash
export OPENAI_API_KEY=your-openai-api-key
```

2. 启动所有服务
```bash
docker-compose -f docker-compose-full.yml up -d
```

3. 访问应用
- 前端: http://localhost:5173
- 后端API: http://localhost:8080
- 数据库: localhost:5432

### 方式二：本地开发

#### 启动数据库
```bash
docker run -d \
  --name rag-postgres \
  -e POSTGRES_DB=rag_db \
  -e POSTGRES_USER=rag_user \
  -e POSTGRES_PASSWORD=rag_password \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  pgvector/pgvector:pg16
```

#### 启动后端
```bash
cd /path/to/rag_vector
export OPENAI_API_KEY=your-openai-api-key
mvn spring-boot:run
```

#### 启动前端
```bash
cd frontend
npm install
npm run dev
```

## 核心功能

### 1. 文档管理
- 支持PDF、TXT等多种文档格式上传
- Agentic RAG智能文档切片
- 文档列表展示和搜索
- 文档删除和状态管理

### 2. RAG智能问答
- 自然语言提问
- 语义相似度检索
- LLM生成答案
- 引用来源展示

### 3. 系统配置
- Embedding模型配置
- LLM模型配置
- 切片策略配置
- 温度参数调整

## API端点

### 文档管理
- `GET /api/documents` - 获取文档列表
- `POST /api/documents/upload` - 上传文档
- `DELETE /api/documents/{id}` - 删除文档
- `GET /api/documents/{id}/chunks` - 获取文档切片

### RAG查询
- `POST /api/rag/query` - RAG查询
- `GET /api/rag/history` - 获取对话历史

### 系统配置
- `GET /api/config` - 获取系统配置
- `PUT /api/config` - 更新系统配置

## 数据库设计

系统使用PostgreSQL + pgvector，包含以下核心表：

- `documents` - 文档元数据
- `document_chunks` - 文档切片（包含向量嵌入）
- `chat_sessions` - 对话会话
- `chat_messages` - 对话消息
- `system_config` - 系统配置

## 开发指南

### 前端开发
```bash
cd frontend
npm run dev          # 开发模式
npm run build        # 构建生产版本
npm run type-check   # 类型检查
```

### 后端开发
```bash
mvn clean install    # 构建项目
mvn spring-boot:run  # 运行应用
mvn test            # 运行测试
```

## 环境变量

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| OPENAI_API_KEY | OpenAI API密钥 | 必填 |
| SPRING_DATASOURCE_URL | 数据库连接URL | jdbc:postgresql://localhost:5432/rag_db |
| SPRING_DATASOURCE_USERNAME | 数据库用户名 | rag_user |
| SPRING_DATASOURCE_PASSWORD | 数据库密码 | rag_password |

## 许可证

MIT License
