# RAG系统与pgvector

基于PostgreSQL + pgvector的检索增强生成(RAG)系统。

## 特性

- 🌲 **支持多种嵌入模型**: 本地sentence-transformers和OpenAI嵌入
- 🧠 **多LLM支持**: OpenAI、Anthropic Claude、Ollama本地模型
- 📚 **文档处理**: 智能文本分块、中英文支持
- 🔍 **向量检索**: 基于pgvector的高效相似性搜索
- 🛠️ **灵活的API**: 命令行工具和Web API

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境

```bash
cp .env.example .env
# 编辑.env文件，配置数据库连接和API密钥
```

### 3. 初始化数据库

确保PostgreSQL已安装并运行，然后安装pgvector扩展：

```sql
CREATE EXTENSION vector;
```

或通过程序自动初始化。

### 4. 基本使用

#### 命令行工具

```bash
# 初始化系统
python main.py init

# 添加文档
python main.py add --text "你的文本内容"

# 从文件添加
python main.py add --file ./documents/sample.txt

# 查询
python main.py query -q "你的问题"

# 交互模式
python main.py interactive
```

#### Python API

```python
from src import initialize_database, RAGPipeline

# 初始化
initialize_database()

# 创建RAG管道
rag = RAGPipeline()

# 添加文档
rag.index_document(
    content="RAG系统是一种结合检索和生成的技术",
    metadata={"source": "技术文档"}
)

# 查询
result = rag.query_with_sources("什么是RAG系统?")
print(result["answer"])
```

#### Web API

```bash
# 启动API服务
python api.py
```

访问 `http://localhost:8000/docs` 查看API文档。

## 项目结构

```
rag_vector/
├── config/
│   └── settings.py          # 配置管理
├── src/
│   ├── database.py          # 数据库连接
│   ├── embedding.py         # 嵌入模型
│   ├── vector_store.py      # 向量存储
│   ├── document.py          # 文档处理
│   ├── rag.py               # RAG管道
│   └── llm.py               # LLM集成
├── main.py                  # CLI工具
├── api.py                   # Web API
└── requirements.txt         # 依赖
```

## 配置说明

### 数据库配置

```python
DATABASE_URL=postgresql://user:pass@localhost:5432/rag_db
```

### 嵌入模型

支持本地模型和OpenAI：

```python
# 本地模型（默认）
LOCAL_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# OpenAI
OPENAI_EMBEDDING_MODEL=text-embedding-ada-002
OPENAI_API_KEY=your-key
```

### LLM配置

支持OpenAI、Anthropic和Ollama：

```python
LLM_PROVIDER=openai  # openai, anthropic, local
MODEL_NAME=gpt-3.5-turbo
```

## 性能优化

- 使用IVFFlat索引加速向量搜索
- 支持批量文档处理
- 连接池管理
- 可配置的向量维度

## 许可证

MIT License
