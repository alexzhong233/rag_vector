"""
FastAPI Web Service for RAG System
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import logging

from src import initialize_database, RAGPipeline

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="RAG API",
    description="RAG System with pgvector",
    version="1.0.0"
)

rag_pipeline = None


@app.on_event("startup")
async def startup_event():
    """应用启动时初始化"""
    global rag_pipeline
    logger.info("Initializing RAG system...")
    initialize_database()
    rag_pipeline = RAGPipeline()
    logger.info("RAG system initialized")


class DocumentInput(BaseModel):
    content: str
    metadata: Optional[Dict[str, Any]] = None


class DocumentBatchInput(BaseModel):
    documents: List[DocumentInput]


class QueryInput(BaseModel):
    question: str
    top_k: Optional[int] = 5
    embedding_provider: Optional[str] = "local"


@app.get("/")
async def root():
    return {"message": "RAG API is running", "docs": "/docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.get("/stats")
async def get_stats():
    """获取系统统计信息"""
    from src import vector_store
    return {
        "total_documents": vector_store.count_documents()
    }


@app.post("/documents")
async def add_document(doc: DocumentInput):
    """添加单个文档"""
    try:
        doc_ids = rag_pipeline.index_document(
            content=doc.content,
            metadata=doc.metadata,
            embedding_provider="local"
        )
        return {
            "success": True,
            "document_ids": doc_ids,
            "message": f"Added {len(doc_ids)} document chunks"
        }
    except Exception as e:
        logger.error(f"Error adding document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/documents/batch")
async def add_documents_batch(docs: DocumentBatchInput):
    """批量添加文档"""
    try:
        documents = [
            {"content": doc.content, "metadata": doc.metadata or {}}
            for doc in docs.documents
        ]
        
        doc_ids = rag_pipeline.index_documents_batch(
            documents=documents,
            embedding_provider="local"
        )
        
        return {
            "success": True,
            "document_ids": doc_ids,
            "message": f"Added {len(doc_ids)} document chunks"
        }
    except Exception as e:
        logger.error(f"Error adding documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/query")
async def query(query_input: QueryInput):
    """查询RAG系统"""
    try:
        result = rag_pipeline.query_with_sources(
            question=query_input.question,
            top_k=query_input.top_k,
            embedding_provider=query_input.embedding_provider
        )
        
        return {
            "success": True,
            "question": result["question"],
            "answer": result["answer"],
            "sources": [
                {
                    "content": source["content"],
                    "metadata": source["metadata"],
                    "similarity": source["similarity"]
                }
                for source in result["sources"]
            ]
        }
    except Exception as e:
        logger.error(f"Error querying: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents/{doc_id}")
async def delete_document(doc_id: int):
    """删除文档"""
    try:
        from src import vector_store
        vector_store.delete_document(doc_id)
        return {
            "success": True,
            "message": f"Deleted document {doc_id}"
        }
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/documents")
async def clear_all_documents():
    """清空所有文档"""
    try:
        from src import vector_store
        vector_store.clear_all()
        return {
            "success": True,
            "message": "Cleared all documents"
        }
    except Exception as e:
        logger.error(f"Error clearing documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
