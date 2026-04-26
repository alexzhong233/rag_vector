"""
RAG系统使用示例
"""

from src import initialize_database, RAGPipeline


def main():
    # 1. 初始化数据库
    print("1. Initializing database...")
    initialize_database()
    
    # 2. 创建RAG管道
    print("2. Creating RAG pipeline...")
    rag = RAGPipeline()
    
    # 3. 添加文档
    print("3. Adding documents...")
    
    documents = [
        {
            "content": """
            RAG (Retrieval-Augmented Generation) is a technique that combines 
            the power of large language models with external knowledge retrieval. 
            It helps reduce hallucinations and provides more accurate, up-to-date responses.
            """,
            "metadata": {"topic": "AI", "type": "technology"}
        },
        {
            "content": """
            PostgreSQL is a powerful, open source object-relational database system.
            It has more than 35 years of active development and has earned a strong reputation 
            for reliability, feature robustness, and performance.
            """,
            "metadata": {"topic": "database", "type": "technology"}
        },
        {
            "content": """
            Vector databases are specialized databases designed to store and query 
            high-dimensional vectors. They are commonly used for similarity search, 
            recommendation systems, and AI applications like RAG.
            """,
            "metadata": {"topic": "database", "type": "technology"}
        }
    ]
    
    doc_ids = rag.index_documents_batch(documents)
    print(f"   Added {len(doc_ids)} document chunks")
    
    # 4. 查询
    print("\n4. Querying the RAG system...")
    print("=" * 80)
    
    questions = [
        "What is RAG and how does it work?",
        "Tell me about PostgreSQL",
        "What are vector databases used for?"
    ]
    
    for question in questions:
        print(f"\nQuestion: {question}")
        print("-" * 80)
        
        result = rag.query_with_sources(question)
        print(f"Answer: {result['answer']}")
        
        if result['sources']:
            print(f"\nSources ({len(result['sources'])} found):")
            for i, source in enumerate(result['sources'][:2], 1):
                print(f"  {i}. {source['content'][:100]}... (similarity: {source['similarity']:.3f})")
        
        print()
    
    print("=" * 80)
    print("Demo completed!")


if __name__ == "__main__":
    main()
