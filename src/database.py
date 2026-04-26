import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from contextlib import contextmanager
from typing import Generator
import logging

from config import settings

logger = logging.getLogger(__name__)


def create_database_if_not_exists():
    """创建数据库（如果不存在）"""
    db_url = settings.database_url
    parts = db_url.replace("postgresql://", "").split("/")
    base_url = "/".join(parts[:-1])
    db_name = parts[-1]
    
    try:
        conn = psycopg2.connect(base_url + "/postgres")
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {db_name}")
            logger.info(f"Database '{db_name}' created successfully")
        else:
            logger.info(f"Database '{db_name}' already exists")
            
        cursor.close()
        conn.close()
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise


def init_pgvector_extension():
    """初始化pgvector扩展"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
        
        # 创建文档表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 创建向量表（使用pgvector）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_embeddings (
                id SERIAL PRIMARY KEY,
                document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
                embedding VECTOR(%s),
                embedding_model VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """, (settings.embedding_dimension,))
        
        # 创建索引以加速相似性搜索
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_embeddings_cosine 
            ON document_embeddings 
            USING ivfflat (embedding vector_cosine_ops)
        """)
        
        conn.commit()
        cursor.close()
        logger.info("pgvector extension and tables initialized successfully")


@contextmanager
def get_connection():
    """获取数据库连接的上下文管理器"""
    conn = None
    try:
        conn = psycopg2.connect(settings.database_url)
        yield conn
    finally:
        if conn:
            conn.close()


@contextmanager
def get_cursor():
    """获取游标的上下文管理器"""
    with get_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()


def initialize_database():
    """初始化数据库：创建数据库和表结构"""
    create_database_if_not_exists()
    init_pgvector_extension()
    logger.info("Database initialization completed")
