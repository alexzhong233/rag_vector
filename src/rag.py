from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

from src.vector_store import vector_store, VectorStore
from src.llm import get_llm, LLMProvider
from src.document import document_processor, DocumentProcessor, DocumentChunk

logger = logging.getLogger(__name__)


@dataclass
class RetrievalResult:
    """检索结果"""
    content: str
    metadata: Dict[str, Any]
    similarity: float
    document_id: int


@dataclass
class RAGResponse:
    """RAG响应"""
    answer: str
    sources: List[RetrievalResult]
    question: str


class RAGPipeline:
    """RAG管道"""
    
    def __init__(
        self,
        vector_store: VectorStore = None,
        llm_provider: LLMProvider = None,
        document_processor: DocumentProcessor = None
    ):
        self.vector_store = vector_store or vector_store
        self.llm = llm_provider or get_llm()
        self.doc_processor = document_processor or document_processor
    
    def index_document(
        self,
        content: str,
        metadata: Dict[str, Any] = None,
        embedding_provider: str = "local",
        chunk: bool = True
    ) -> List[int]:
        """索引文档"""
        if chunk:
            # 分块处理
            chunks = self.doc_processor.process_text(content, metadata)
            
            documents = [
                {
                    "content": chunk.content,
                    "metadata": {
                        **chunk.metadata,
                        "chunk_index": chunk.chunk_index
                    }
                }
                for chunk in chunks
            ]
            
            return self.vector_store.add_documents_batch(
                documents,
                embedding_provider=embedding_provider
            )
        else:
            # 不分块，直接添加
            return [self.vector_store.add_document(
                content,
                metadata,
                embedding_provider
            )]
    
    def index_file(
        self,
        file_path: str,
        embedding_provider: str = "local",
        metadata: Dict[str, Any] = None
    ) -> List[int]:
        """索引文件"""
        chunks = self.doc_processor.load_and_process_file(file_path, metadata)
        
        documents = [
            {
                "content": chunk.content,
                "metadata": chunk.metadata
            }
            for chunk in chunks
        ]
        
        return self.vector_store.add_documents_batch(
            documents,
            embedding_provider=embedding_provider
        )
    
    def index_documents_batch(
        self,
        documents: List[Dict[str, Any]],
        embedding_provider: str = "local"
    ) -> List[int]:
        """批量索引文档"""
        # 处理每个文档
        processed_docs = []
        for doc in documents:
            content = doc.get("content", "")
            metadata = doc.get("metadata", {})
            
            chunks = self.doc_processor.process_text(content, metadata)
            
            for chunk in chunks:
                processed_docs.append({
                    "content": chunk.content,
                    "metadata": chunk.metadata
                })
        
        return self.vector_store.add_documents_batch(
            processed_docs,
            embedding_provider=embedding_provider
        )
    
    def retrieve(
        self,
        query: str,
        top_k: int = None,
        embedding_provider: str = "local",
        filter_metadata: Dict[str, Any] = None
    ) -> List[RetrievalResult]:
        """检索相关文档"""
        results = self.vector_store.similarity_search(
            query=query,
            top_k=top_k,
            embedding_provider=embedding_provider,
            filter_metadata=filter_metadata,
            return_scores=True
        )
        
        return [
            RetrievalResult(
                content=result["content"],
                metadata=result["metadata"],
                similarity=result["similarity"],
                document_id=result["id"]
            )
            for result in results
        ]
    
    def generate_answer(
        self,
        query: str,
        context: str,
        system_prompt: str = None
    ) -> str:
        """生成答案"""
        if system_prompt is None:
            system_prompt = """You are a helpful AI assistant. Based on the provided context, answer the user's question accurately and concisely. If the context doesn't contain relevant information, say so rather than making up an answer."""
        
        prompt = f"""Context:
{context}

Question: {query}

Answer:"""
        
        return self.llm.generate(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=0.7,
            max_tokens=1000
        )
    
    def query(
        self,
        question: str,
        top_k: int = None,
        embedding_provider: str = "local",
        filter_metadata: Dict[str, Any] = None,
        return_sources: bool = True,
        system_prompt: str = None
    ) -> RAGResponse:
        """完整的RAG查询"""
        # 1. 检索相关文档
        retrieval_results = self.retrieve(
            query=question,
            top_k=top_k,
            embedding_provider=embedding_provider,
            filter_metadata=filter_metadata
        )
        
        if not retrieval_results:
            return RAGResponse(
                answer="No relevant documents found for your question.",
                sources=[],
                question=question
            )
        
        # 2. 构建上下文
        context_parts = []
        for i, result in enumerate(retrieval_results, 1):
            context_parts.append(f"[Document {i}]\n{result.content}")
        
        context = "\n\n".join(context_parts)
        
        # 3. 生成答案
        answer = self.generate_answer(
            query=question,
            context=context,
            system_prompt=system_prompt
        )
        
        # 4. 返回结果
        return RAGResponse(
            answer=answer,
            sources=retrieval_results if return_sources else [],
            question=question
        )
    
    def query_with_sources(
        self,
        question: str,
        top_k: int = None,
        embedding_provider: str = "local"
    ) -> Dict[str, Any]:
        """查询并返回详细结果"""
        response = self.query(
            question=question,
            top_k=top_k,
            embedding_provider=embedding_provider,
            return_sources=True
        )
        
        return {
            "question": response.question,
            "answer": response.answer,
            "sources": [
                {
                    "content": source.content,
                    "metadata": source.metadata,
                    "similarity": source.similarity,
                    "document_id": source.document_id
                }
                for source in response.sources
            ]
        }


# 全局RAG管道实例
rag_pipeline = RAGPipeline()
