import json
from typing import List, Dict, Any, Optional, Tuple
import logging

from src.database import get_cursor, get_connection
from src.embedding import embedding_service, get_embedding_model, EmbeddingModel
from config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """向量存储管理类"""
    
    def __init__(self, embedding_model: EmbeddingModel = None):
        self.embedding_model = embedding_model or get_embedding_model()
        self.dimension = self.embedding_model.dimension
        
    def add_document(
        self, 
        content: str, 
        metadata: Dict[str, Any] = None,
        embedding_provider: str = "local"
    ) -> int:
        """添加文档并生成嵌入向量"""
        # 生成嵌入向量
        embedding = embedding_service.embed_with_provider(content, provider=embedding_provider)
        
        with get_cursor() as cursor:
            # 插入文档
            cursor.execute(
                "INSERT INTO documents (content, metadata) VALUES (%s, %s) RETURNING id",
                (content, json.dumps(metadata) if metadata else None)
            )
            doc_id = cursor.fetchone()[0]
            
            # 插入嵌入向量
            cursor.execute(
                """
                INSERT INTO document_embeddings (document_id, embedding, embedding_model)
                VALUES (%s, %s, %s)
                """,
                (doc_id, embedding, embedding_provider)
            )
            
        logger.info(f"Added document with id: {doc_id}")
        return doc_id
    
    def add_documents_batch(
        self,
        documents: List[Dict[str, Any]],
        embedding_provider: str = "local",
        show_progress: bool = True
    ) -> List[int]:
        """批量添加文档"""
        doc_ids = []
        contents = [doc["content"] for doc in documents]
        
        # 批量生成嵌入
        embeddings = embedding_service.embed_batch_with_provider(
            contents, 
            provider=embedding_provider
        )
        
        with get_connection() as conn:
            cursor = conn.cursor()
            
            for i, doc in enumerate(documents):
                # 插入文档
                cursor.execute(
                    "INSERT INTO documents (content, metadata) VALUES (%s, %s) RETURNING id",
                    (doc["content"], json.dumps(doc.get("metadata")))
                )
                doc_id = cursor.fetchone()[0]
                doc_ids.append(doc_id)
                
                # 插入嵌入向量
                cursor.execute(
                    """
                    INSERT INTO document_embeddings (document_id, embedding, embedding_model)
                    VALUES (%s, %s, %s)
                    """,
                    (doc_id, embeddings[i], embedding_provider)
                )
                
                if show_progress and (i + 1) % 100 == 0:
                    logger.info(f"Processed {i + 1}/{len(documents)} documents")
            
            conn.commit()
            cursor.close()
        
        logger.info(f"Batch added {len(doc_ids)} documents")
        return doc_ids
    
    def similarity_search(
        self,
        query: str,
        top_k: int = None,
        embedding_provider: str = "local",
        filter_metadata: Dict[str, Any] = None,
        return_scores: bool = False
    ) -> List[Dict[str, Any]]:
        """执行相似性搜索"""
        top_k = top_k or settings.default_top_k
        
        # 生成查询向量
        query_embedding = embedding_service.embed_with_provider(query, provider=embedding_provider)
        
        # 确定距离函数
        distance_func = "cosine_distance" if settings.distance_function == "cosine" else "l2_distance"
        
        sql = f"""
            SELECT 
                d.id,
                d.content,
                d.metadata,
                1 - e.embedding <=> %s::vector AS similarity
            FROM documents d
            JOIN document_embeddings e ON d.id = e.document_id
            WHERE e.embedding_model = %s
        """
        
        # 添加元数据过滤
        if filter_metadata:
            for key, value in filter_metadata.items():
                sql += f" AND d.metadata->>%s = %s"
                filter_metadata_list = [(k, v) for k, v in filter_metadata.items()]
        
        sql += f"""
            ORDER BY e.embedding <=> %s::vector
            LIMIT %s
        """
        
        # 构建参数
        params = [query_embedding, embedding_provider]
        if filter_metadata:
            for key, value in filter_metadata.items():
                params.extend([key, str(value)])
        params.extend([query_embedding, top_k])
        
        with get_cursor() as cursor:
            cursor.execute(sql, params)
            results = cursor.fetchall()
        
        # 格式化结果
        documents = []
        for row in results:
            doc = {
                "id": row[0],
                "content": row[1],
                "metadata": json.loads(row[2]) if row[2] else {},
            }
            if return_scores:
                doc["similarity"] = row[3]
            documents.append(doc)
        
        return documents
    
    def get_document_by_id(self, doc_id: int) -> Optional[Dict[str, Any]]:
        """根据ID获取文档"""
        with get_cursor() as cursor:
            cursor.execute(
                """
                SELECT id, content, metadata, created_at
                FROM documents
                WHERE id = %s
                """,
                (doc_id,)
            )
            row = cursor.fetchone()
            
            if row:
                return {
                    "id": row[0],
                    "content": row[1],
                    "metadata": json.loads(row[2]) if row[2] else {},
                    "created_at": row[3]
                }
        return None
    
    def delete_document(self, doc_id: int):
        """删除文档及其嵌入向量"""
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM documents WHERE id = %s", (doc_id,))
            if cursor.rowcount == 0:
                logger.warning(f"Document {doc_id} not found")
            else:
                logger.info(f"Deleted document {doc_id}")
    
    def update_document(
        self,
        doc_id: int,
        content: str = None,
        metadata: Dict[str, Any] = None,
        embedding_provider: str = "local"
    ):
        """更新文档"""
        if content:
            # 重新生成嵌入
            new_embedding = embedding_service.embed_with_provider(content, provider=embedding_provider)
            
            with get_cursor() as cursor:
                # 更新文档
                cursor.execute(
                    "UPDATE documents SET content = %s, metadata = %s WHERE id = %s",
                    (content, json.dumps(metadata), doc_id)
                )
                
                # 更新嵌入向量
                cursor.execute(
                    """
                    UPDATE document_embeddings 
                    SET embedding = %s, embedding_model = %s
                    WHERE document_id = %s
                    """,
                    (new_embedding, embedding_provider, doc_id)
                )
                
            logger.info(f"Updated document {doc_id}")
    
    def count_documents(self) -> int:
        """统计文档数量"""
        with get_cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM documents")
            return cursor.fetchone()[0]
    
    def clear_all(self):
        """清空所有文档"""
        with get_cursor() as cursor:
            cursor.execute("DELETE FROM documents")
            cursor.execute("DELETE FROM document_embeddings")
        logger.info("Cleared all documents")


# 全局向量存储实例
vector_store = VectorStore()
