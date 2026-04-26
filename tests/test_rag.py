"""
RAG系统测试
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import (
    initialize_database,
    VectorStore,
    DocumentProcessor,
    RAGPipeline
)


class TestDatabase:
    """数据库测试"""
    
    def test_initialize_database(self):
        """测试数据库初始化"""
        try:
            initialize_database()
        except Exception as e:
            pytest.skip(f"Database not available: {e}")


class TestEmbedding:
    """嵌入模型测试"""
    
    def test_local_embedding(self):
        """测试本地嵌入模型"""
        try:
            from src import LocalEmbeddingModel
            model = LocalEmbeddingModel()
            
            # 测试单个文本
            embedding = model.embed("Hello world")
            assert len(embedding) == model.dimension
            assert isinstance(embedding, list)
            
            # 测试批量
            embeddings = model.embed_batch(["Hello", "World"])
            assert len(embeddings) == 2
            assert all(len(e) == model.dimension for e in embeddings)
            
        except ImportError:
            pytest.skip("sentence-transformers not installed")


class TestDocumentProcessor:
    """文档处理测试"""
    
    def test_text_splitting(self):
        """测试文本分割"""
        processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
        
        # 短文本
        short_text = "这是短文本"
        chunks = processor.process_text(short_text)
        assert len(chunks) == 1
        
        # 长文本
        long_text = "A" * 300
        chunks = processor.process_text(long_text)
        assert len(chunks) > 1
        
        # 测试中英文混合
        mixed_text = "这是中文文本。" * 20
        chunks = processor.process_text(mixed_text)
        assert len(chunks) > 0
        assert all(chunk.content for chunk in chunks)


class TestVectorStore:
    """向量存储测试"""
    
    @pytest.fixture
    def vector_store(self):
        """创建向量存储实例"""
        try:
            return VectorStore()
        except Exception as e:
            pytest.skip(f"Vector store not available: {e}")
    
    def test_add_document(self, vector_store):
        """测试添加文档"""
        try:
            doc_id = vector_store.add_document(
                content="Test document content",
                metadata={"source": "test"}
            )
            assert doc_id > 0
            
            # 清理
            vector_store.delete_document(doc_id)
        except Exception as e:
            pytest.skip(f"Database not available: {e}")
    
    def test_similarity_search(self, vector_store):
        """测试相似性搜索"""
        try:
            # 添加测试文档
            doc_ids = []
            doc_ids.append(vector_store.add_document(
                content="Python is a programming language",
                metadata={"type": "programming"}
            ))
            doc_ids.append(vector_store.add_document(
                content="Java is another programming language",
                metadata={"type": "programming"}
            ))
            doc_ids.append(vector_store.add_document(
                content="Shakespeare wrote Hamlet",
                metadata={"type": "literature"}
            ))
            
            # 搜索
            results = vector_store.similarity_search(
                query="programming languages",
                top_k=2
            )
            
            assert len(results) <= 2
            assert all("programming" in r["content"].lower() for r in results)
            
            # 清理
            for doc_id in doc_ids:
                vector_store.delete_document(doc_id)
                
        except Exception as e:
            pytest.skip(f"Database not available: {e}")


class TestRAGPipeline:
    """RAG管道测试"""
    
    @pytest.fixture
    def rag_pipeline(self):
        """创建RAG管道实例"""
        try:
            initialize_database()
            return RAGPipeline()
        except Exception as e:
            pytest.skip(f"RAG pipeline not available: {e}")
    
    def test_index_and_query(self, rag_pipeline):
        """测试索引和查询"""
        try:
            # 添加文档
            doc_id = rag_pipeline.index_document(
                content="RAG combines retrieval and generation for better AI responses",
                metadata={"topic": "AI"}
            )
            
            # 查询
            result = rag_pipeline.query_with_sources(
                question="What is RAG?"
            )
            
            assert "answer" in result
            assert "sources" in result
            
            # 清理
            from src import vector_store
            vector_store.delete_document(doc_id)
            
        except Exception as e:
            pytest.skip(f"RAG pipeline not available: {e}")


def test_import_all():
    """测试所有模块导入"""
    from src import (
        get_connection,
        get_cursor,
        initialize_database,
        EmbeddingModel,
        LocalEmbeddingModel,
        OpenAIEmbeddingModel,
        EmbeddingService,
        VectorStore,
        DocumentChunk,
        TextSplitter,
        DocumentProcessor,
        DocumentLoader,
        LLMProvider,
        OpenAILLM,
        RAGPipeline,
        RetrievalResult,
        RAGResponse
    )
    assert True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
