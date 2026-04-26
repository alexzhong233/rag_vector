from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import logging

from config import settings

logger = logging.getLogger(__name__)


class LLMProvider(ABC):
    """LLM提供者抽象基类"""
    
    @abstractmethod
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """生成响应"""
        pass
    
    @abstractmethod
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """聊天接口"""
        pass


class OpenAILLM(LLMProvider):
    """OpenAI LLM"""
    
    def __init__(self, api_key: str = None, model: str = None):
        try:
            from openai import OpenAI
            api_key = api_key or settings.openai_api_key
            self.client = OpenAI(api_key=api_key)
            self.model = model or settings.model_name
            logger.info(f"Initialized OpenAI LLM with model: {self.model}")
        except ImportError:
            logger.error("openai not installed. Run: pip install openai")
            raise
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """使用generate接口"""
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages, temperature, max_tokens, **kwargs)
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """使用chat接口"""
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
        return response.choices[0].message.content


class AnthropicLLM(LLMProvider):
    """Anthropic Claude LLM"""
    
    def __init__(self, api_key: str = None, model: str = "claude-3-sonnet-20240229"):
        try:
            import anthropic
            api_key = api_key or settings.anthropic_api_key
            self.client = anthropic.Anthropic(api_key=api_key)
            self.model = model
            logger.info(f"Initialized Anthropic LLM with model: {self.model}")
        except ImportError:
            logger.error("anthropic not installed. Run: pip install anthropic")
            raise
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """生成响应"""
        messages = []
        if system_prompt:
            messages.append({"role": "user", "content": system_prompt + "\n\n" + prompt})
        else:
            messages.append({"role": "user", "content": prompt})
        
        return self.chat(messages, temperature, max_tokens, **kwargs)
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """聊天接口"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            messages=messages,
            temperature=temperature,
            **kwargs
        )
        return response.content[0].text


class OllamaLLM(LLMProvider):
    """Ollama本地LLM"""
    
    def __init__(self, model: str = "llama2", base_url: str = "http://localhost:11434"):
        self.model = model
        self.base_url = base_url
        logger.info(f"Initialized Ollama LLM with model: {self.model}")
    
    def generate(
        self,
        prompt: str,
        system_prompt: str = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """生成响应"""
        import requests
        
        full_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json={
                "model": self.model,
                "prompt": full_prompt,
                "temperature": temperature,
                "options": {"num_predict": max_tokens}
            }
        )
        
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            raise Exception(f"Ollama API error: {response.status_code}")
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """聊天接口"""
        import requests
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={
                "model": self.model,
                "messages": messages,
                "temperature": temperature,
                "options": {"num_predict": max_tokens}
            }
        )
        
        if response.status_code == 200:
            return response.json().get("message", {}).get("content", "")
        else:
            raise Exception(f"Ollama API error: {response.status_code}")


def get_llm_provider(provider: str = None) -> LLMProvider:
    """工厂函数：获取LLM提供者"""
    provider = provider or settings.llm_provider
    
    if provider == "openai":
        return OpenAILLM()
    elif provider == "anthropic":
        return AnthropicLLM()
    elif provider == "local" or provider == "ollama":
        return OllamaLLM()
    else:
        raise ValueError(f"Unknown LLM provider: {provider}")


# 全局LLM实例
llm_provider = None


def get_llm() -> LLMProvider:
    """获取LLM实例"""
    global llm_provider
    if llm_provider is None:
        llm_provider = get_llm_provider()
    return llm_provider
