import numpy as np
from abc import ABC, abstractmethod
from typing import List, Union
import logging

from config import settings

logger = logging.getLogger(__name__)


class EmbeddingModel(ABC):
    """嵌入模型抽象基类"""
    
    @abstractmethod
    def embed(self, text: str) -> List[float]:
        """将文本转换为嵌入向量"""
        pass
    
    @abstractmethod
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """批量将文本转换为嵌入向量"""
        pass
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """返回嵌入向量的维度"""
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        """返回模型名称"""
        pass


class LocalEmbeddingModel(EmbeddingModel):
    """本地嵌入模型（使用sentence-transformers）"""
    
    def __init__(self, model_name: str = None):
        model_name = model_name or settings.local_embedding_model
        try:
            from sentence_transformers import SentenceTransformer
            self.model = SentenceTransformer(model_name)
            self._model_name = model_name
            logger.info(f"Loaded local embedding model: {model_name}")
        except ImportError:
            logger.error("sentence-transformers not installed. Run: pip install sentence-transformers")
            raise
    
    def embed(self, text: str) -> List[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        embeddings = self.model.encode(texts)
        return embeddings.tolist()
    
    @property
    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
    
    @property
    def model_name(self) -> str:
        return self._model_name


class OpenAIEmbeddingModel(EmbeddingModel):
    """OpenAI嵌入模型"""
    
    def __init__(self, model_name: str = None, api_key: str = None):
        model_name = model_name or settings.openai_embedding_model
        api_key = api_key or settings.openai_api_key
        
        try:
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
            self._model_name = model_name
            self._dimension = 1536 if "ada" in model_name else 3072
            logger.info(f"Initialized OpenAI embedding model: {model_name}")
        except ImportError:
            logger.error("openai not installed. Run: pip install openai")
            raise
    
    def embed(self, text: str) -> List[float]:
        response = self.client.embeddings.create(
            model=self._model_name,
            input=text
        )
        return response.data[0].embedding
    
    def embed_batch(self, texts: List[str], batch_size: int = 100) -> List[List[float]]:
        all_embeddings = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            response = self.client.embeddings.create(
                model=self._model_name,
                input=batch
            )
            all_embeddings.extend([item.embedding for item in response.data])
        return all_embeddings
    
    @property
    def dimension(self) -> int:
        return self._dimension
    
    @property
    def model_name(self) -> str:
        return self._model_name


def get_embedding_model(provider: str = None) -> EmbeddingModel:
    """工厂函数：根据配置返回嵌入模型"""
    provider = provider or settings.embedding_provider
    
    if provider == "local":
        return LocalEmbeddingModel()
    elif provider == "openai":
        return OpenAIEmbeddingModel()
    elif provider == "both":
        # 默认返回本地模型，可通过环境变量切换
        try:
            return LocalEmbeddingModel()
        except ImportError:
            logger.warning("Local model not available, falling back to OpenAI")
            return OpenAIEmbeddingModel()
    else:
        raise ValueError(f"Unknown embedding provider: {provider}")


class EmbeddingService:
    """嵌入服务，管理多个嵌入模型"""
    
    def __init__(self):
        self.local_model = None
        self.openai_model = None
        
    def get_local_model(self) -> LocalEmbeddingModel:
        if self.local_model is None:
            self.local_model = LocalEmbeddingModel()
        return self.local_model
    
    def get_openai_model(self) -> OpenAIEmbeddingModel:
        if self.openai_model is None:
            self.openai_model = OpenAIEmbeddingModel()
        return self.openai_model
    
    def embed_with_provider(self, text: str, provider: str = "local") -> List[float]:
        """使用指定provider进行嵌入"""
        if provider == "local":
            return self.get_local_model().embed(text)
        elif provider == "openai":
            return self.get_openai_model().embed(text)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    
    def embed_batch_with_provider(self, texts: List[str], provider: str = "local") -> List[List[float]]:
        """批量嵌入"""
        if provider == "local":
            return self.get_local_model().embed_batch(texts)
        elif provider == "openai":
            return self.get_openai_model().embed_batch(texts)
        else:
            raise ValueError(f"Unknown provider: {provider}")


# 全局嵌入服务实例
embedding_service = EmbeddingService()
