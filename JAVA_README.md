# RAG Vector - Java Spring Boot 版本

这是一个基于Java Spring Boot 3.2的RAG（检索增强生成）系统，使用PostgreSQL + pgvector进行向量存储。

## 技术栈

- Java 17
- Spring Boot 3.2
- Spring Data JPA
- PostgreSQL
- pgvector (向量数据库)
- LangChain4j (LLM集成)
- Apache PDFBox (PDF处理)
- Lombok

## 项目结构

```
src/main/java/com/rag/
├── config/           # 配置类
├── controller/       # 控制器
├── dto/            # 数据传输对象
├── entity/         # 实体类
├── repository/     # 数据访问层
├── service/         # 业务逻辑层
└── RagApplication.java  # 主应用类
```

## 数据库设置

1. 首先需要PostgreSQL数据库
2. 创建数据库：`rag_db`
3. 确保pgvector扩展已安装

初始化脚本位置：`src/main/resources/schema.sql`

## 配置

在 `application.yml` 中配置：
- 数据库连接信息
- OpenAI API密钥
- RAG参数（分块大小、重叠、Top-K）

## API端点

### 文档管理
- `GET /api/documents` - 获取所有文档
- `GET /api/documents/{id}` - 获取单个文档
- `POST /api/documents/upload` - 上传文档
- `DELETE /api/documents/{id}` - 删除文档

### RAG查询
- `POST /api/rag/query` - RAG查询

### 配置管理
- `GET /api/config` - 获取所有配置
- `GET /api/config/{configKey}` - 获取单个配置
- `PUT /api/config` - 更新配置
- `DELETE /api/config/{id}` - 删除配置

## 运行项目

```bash
mvn spring-boot:run
```

## 构建项目

```bash
mvn clean package
```
