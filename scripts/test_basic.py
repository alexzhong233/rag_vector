#!/usr/bin/env python3
"""
简单的测试脚本，验证RAG系统的基本功能
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_imports():
    """测试模块导入"""
    print("Testing imports...")
    try:
        from src import (
            initialize_database,
            VectorStore,
            RAGPipeline,
            LocalEmbeddingModel
        )
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False


def test_embedding_model():
    """测试嵌入模型"""
    print("\nTesting embedding model...")
    try:
        from src import LocalEmbeddingModel
        
        model = LocalEmbeddingModel()
        embedding = model.embed("Hello world")
        
        print(f"✓ Generated embedding with dimension: {len(embedding)}")
        return True
    except Exception as e:
        print(f"✗ Embedding test failed: {e}")
        return False


def test_document_processing():
    """测试文档处理"""
    print("\nTesting document processing...")
    try:
        from src import DocumentProcessor
        
        processor = DocumentProcessor(chunk_size=100, chunk_overlap=20)
        text = "This is a test document. " * 10
        
        chunks = processor.process_text(text)
        
        print(f"✓ Split text into {len(chunks)} chunks")
        return True
    except Exception as e:
        print(f"✗ Document processing failed: {e}")
        return False


def main():
    """运行所有测试"""
    print("=" * 60)
    print("RAG System Basic Tests")
    print("=" * 60)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Embedding Model", test_embedding_model()))
    results.append(("Document Processing", test_document_processing()))
    
    print("\n" + "=" * 60)
    print("Test Results:")
    print("=" * 60)
    
    for name, passed in results:
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{name:.<40} {status}")
    
    all_passed = all(passed for _, passed in results)
    
    print("=" * 60)
    if all_passed:
        print("All tests passed! ✓")
        print("\nNext steps:")
        print("1. Start PostgreSQL with pgvector (see docker-compose.yml)")
        print("2. Configure your .env file")
        print("3. Run: python main.py init")
        print("4. Run: python examples/quickstart.py")
    else:
        print("Some tests failed. Please check the errors above.")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
