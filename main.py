#!/usr/bin/env python3
"""
RAG系统主程序
支持命令行交互和API服务
"""

import sys
import argparse
import logging
from typing import Optional

from config import settings
from src import (
    initialize_database,
    RAGPipeline,
    DocumentLoader,
    DocumentProcessor
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def init_system():
    """初始化系统"""
    logger.info("Initializing RAG system...")
    try:
        initialize_database()
        logger.info("System initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize system: {e}")
        raise


def add_document_from_text(
    text: str,
    metadata: dict = None,
    embedding_provider: str = "local"
):
    """从文本添加文档"""
    init_system()
    rag = RAGPipeline()
    
    doc_ids = rag.index_document(
        content=text,
        metadata=metadata,
        embedding_provider=embedding_provider
    )
    
    logger.info(f"Added document with IDs: {doc_ids}")
    return doc_ids


def add_document_from_file(
    file_path: str,
    embedding_provider: str = "local",
    metadata: dict = None
):
    """从文件添加文档"""
    init_system()
    rag = RAGPipeline()
    
    doc_ids = rag.index_file(
        file_path=file_path,
        embedding_provider=embedding_provider,
        metadata=metadata
    )
    
    logger.info(f"Indexed file with {len(doc_ids)} chunks")
    return doc_ids


def add_documents_from_directory(
    directory: str,
    embedding_provider: str = "local"
):
    """从目录批量添加文档"""
    init_system()
    rag = RAGPipeline()
    
    documents = DocumentLoader.load_directory(directory)
    logger.info(f"Loaded {len(documents)} documents from directory")
    
    doc_ids = rag.index_documents_batch(
        documents=documents,
        embedding_provider=embedding_provider
    )
    
    logger.info(f"Indexed {len(doc_ids)} document chunks")
    return doc_ids


def query_system(
    question: str,
    top_k: int = 5,
    embedding_provider: str = "local",
    show_sources: bool = True
):
    """查询系统"""
    init_system()
    rag = RAGPipeline()
    
    result = rag.query_with_sources(
        question=question,
        top_k=top_k,
        embedding_provider=embedding_provider
    )
    
    print("\n" + "="*80)
    print(f"Question: {result['question']}")
    print("="*80)
    print(f"\nAnswer:\n{result['answer']}")
    
    if show_sources and result['sources']:
        print("\n" + "="*80)
        print("Sources:")
        print("="*80)
        for i, source in enumerate(result['sources'], 1):
            print(f"\n[Source {i}] (Similarity: {source['similarity']:.4f})")
            print(f"Content: {source['content'][:200]}...")
            if source['metadata']:
                print(f"Metadata: {source['metadata']}")
    
    return result


def interactive_mode():
    """交互模式"""
    print("\n" + "="*80)
    print("RAG System Interactive Mode")
    print("="*80)
    print("Commands:")
    print("  - Type your question and press Enter to query")
    print("  - Type 'quit' or 'exit' to exit")
    print("  - Type 'stats' to show statistics")
    print("="*80 + "\n")
    
    init_system()
    rag = RAGPipeline()
    
    while True:
        try:
            question = input("You: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            if question.lower() == 'stats':
                from src import vector_store
                count = vector_store.count_documents()
                print(f"Total documents: {count}")
                continue
            
            if not question:
                continue
            
            result = rag.query_with_sources(
                question=question,
                top_k=5
            )
            
            print(f"\nAssistant: {result['answer']}\n")
            
            if result['sources']:
                print("Sources:")
                for i, source in enumerate(result['sources'][:3], 1):
                    print(f"  {i}. {source['content'][:100]}... (score: {source['similarity']:.3f})")
            
            print()
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            logger.error(f"Error: {e}")
            print(f"Error: {e}\n")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="RAG System with pgvector")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # init命令
    subparsers.add_parser("init", help="Initialize the RAG system")
    
    # add命令
    add_parser = subparsers.add_parser("add", help="Add documents")
    add_parser.add_argument("-t", "--text", help="Text content to add")
    add_parser.add_argument("-f", "--file", help="File path to add")
    add_parser.add_argument("-d", "--directory", help="Directory path to add")
    add_parser.add_argument("--provider", choices=["local", "openai"], 
                           default="local", help="Embedding provider")
    
    # query命令
    query_parser = subparsers.add_parser("query", help="Query the RAG system")
    query_parser.add_argument("-q", "--question", required=True, help="Question to ask")
    query_parser.add_argument("-k", "--top-k", type=int, default=5, help="Number of results")
    query_parser.add_argument("--provider", choices=["local", "openai"],
                             default="local", help="Embedding provider")
    query_parser.add_argument("--no-sources", action="store_true", help="Hide sources")
    
    # interactive命令
    subparsers.add_parser("interactive", help="Start interactive mode")
    
    args = parser.parse_args()
    
    if args.command == "init":
        init_system()
        
    elif args.command == "add":
        if args.text:
            add_document_from_text(args.text, embedding_provider=args.provider)
        elif args.file:
            add_document_from_file(args.file, embedding_provider=args.provider)
        elif args.directory:
            add_documents_from_directory(args.directory, embedding_provider=args.provider)
        else:
            print("Please specify --text, --file, or --directory")
            
    elif args.command == "query":
        query_system(
            question=args.question,
            top_k=args.top_k,
            embedding_provider=args.provider,
            show_sources=not args.no_sources
        )
        
    elif args.command == "interactive":
        interactive_mode()
        
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
