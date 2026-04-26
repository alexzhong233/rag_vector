import os
from typing import Literal
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database settings
    database_url: str = "postgresql://postgres:postgres@localhost:5432/rag_db"
    
    # Embedding settings
    embedding_provider: Literal["local", "openai", "both"] = "both"
    local_embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2"
    openai_embedding_model: str = "text-embedding-ada-002"
    openai_api_key: str = ""
    
    # LLM settings
    llm_provider: Literal["openai", "anthropic", "local"] = "openai"
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    model_name: str = "gpt-3.5-turbo"
    
    # Vector store settings
    embedding_dimension: int = 384  # Default for all-MiniLM-L6-v2
    distance_function: str = "cosine"  # cosine, l2, or ip
    
    # RAG settings
    default_top_k: int = 5
    default_chunk_size: int = 500
    default_chunk_overlap: int = 50
    
    class Config:
        env_file = ".env"
        extra = "allow"


settings = Settings()
