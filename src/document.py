import re
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
import logging

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class DocumentChunk:
    """文档块数据结构"""
    content: str
    metadata: Dict[str, Any]
    chunk_index: int
    start_char: int
    end_char: int


class TextSplitter:
    """文本分割器"""
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
        length_function: Callable[[str], int] = len
    ):
        self.chunk_size = chunk_size or settings.default_chunk_size
        self.chunk_overlap = chunk_overlap or settings.default_chunk_overlap
        self.length_function = length_function
    
    def split_text(self, text: str, metadata: Dict[str, Any] = None) -> List[DocumentChunk]:
        """分割文本为块"""
        if self.length_function(text) <= self.chunk_size:
            return [DocumentChunk(
                content=text,
                metadata=metadata or {},
                chunk_index=0,
                start_char=0,
                end_char=len(text)
            )]
        
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # 尽量在句子边界分割
            if end < len(text):
                # 向前查找最近的句子边界
                boundary = self._find_sentence_boundary(text, start, end)
                if boundary > start:
                    end = boundary
            
            chunk_text = text[start:end]
            chunk_text = chunk_text.strip()
            
            if chunk_text:
                chunks.append(DocumentChunk(
                    content=chunk_text,
                    metadata=metadata or {},
                    chunk_index=chunk_index,
                    start_char=start,
                    end_char=end
                ))
            
            start = end - self.chunk_overlap
            chunk_index += 1
            
            if start >= len(text):
                break
        
        return chunks
    
    def _find_sentence_boundary(self, text: str, start: int, end: int) -> int:
        """查找句子边界"""
        # 中英文句子结束符
        sentence_endings = r'[。！？.!?\n]+'
        
        # 在end附近查找句子边界
        search_start = max(start, end - 100)
        segment = text[search_start:end]
        
        matches = list(re.finditer(sentence_endings, segment))
        if matches:
            last_match = matches[-1]
            return search_start + last_match.end()
        
        # 如果没找到，在end处查找空格
        space_idx = segment.rfind(' ')
        if space_idx != -1:
            return search_start + space_idx + 1
        
        return end


class DocumentProcessor:
    """文档处理器"""
    
    def __init__(
        self,
        chunk_size: int = None,
        chunk_overlap: int = None,
        remove_extra_whitespace: bool = True,
        strip_newlines: bool = False
    ):
        self.text_splitter = TextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        self.remove_extra_whitespace = remove_extra_whitespace
        self.strip_newlines = strip_newlines
    
    def process_text(
        self,
        text: str,
        metadata: Dict[str, Any] = None
    ) -> List[DocumentChunk]:
        """处理单个文本"""
        # 预处理
        if self.remove_extra_whitespace:
            text = re.sub(r'\s+', ' ', text)
        
        if self.strip_newlines:
            text = text.replace('\n', ' ').replace('\r', ' ')
        
        # 分割
        return self.text_splitter.split_text(text, metadata)
    
    def process_documents(
        self,
        documents: List[Dict[str, Any]],
        metadata_field: str = "metadata"
    ) -> List[DocumentChunk]:
        """批量处理文档"""
        all_chunks = []
        
        for doc in documents:
            text = doc.get("content", "")
            metadata = doc.get(metadata_field, {})
            
            # 添加源文档信息到metadata
            if "source" in doc:
                metadata["source"] = doc["source"]
            if "title" in doc:
                metadata["title"] = doc["title"]
            
            chunks = self.process_text(text, metadata)
            all_chunks.extend(chunks)
        
        return all_chunks
    
    def load_file(self, file_path: str) -> str:
        """加载文本文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def load_and_process_file(
        self,
        file_path: str,
        metadata: Dict[str, Any] = None
    ) -> List[DocumentChunk]:
        """加载并处理文件"""
        text = self.load_file(file_path)
        
        metadata = metadata or {}
        metadata["source"] = file_path
        
        return self.process_text(text, metadata)


class DocumentLoader:
    """文档加载器"""
    
    @staticmethod
    def load_text_file(file_path: str) -> Dict[str, Any]:
        """加载文本文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        return {
            "content": content,
            "metadata": {
                "source": file_path,
                "type": "text"
            }
        }
    
    @staticmethod
    def load_markdown(file_path: str) -> Dict[str, Any]:
        """加载Markdown文件"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 提取标题作为title
        title_match = re.match(r'^#\s+(.+)$', content, re.MULTILINE)
        title = title_match.group(1) if title_match else ""
        
        return {
            "content": content,
            "metadata": {
                "source": file_path,
                "type": "markdown",
                "title": title
            }
        }
    
    @staticmethod
    def load_directory(
        directory_path: str,
        extensions: List[str] = ['.txt', '.md', '.text']
    ) -> List[Dict[str, Any]]:
        """加载目录下的所有文件"""
        import os
        documents = []
        
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    try:
                        if file.endswith('.md'):
                            doc = DocumentLoader.load_markdown(file_path)
                        else:
                            doc = DocumentLoader.load_text_file(file_path)
                        documents.append(doc)
                    except Exception as e:
                        logger.error(f"Error loading file {file_path}: {e}")
        
        return documents


# 全局文档处理器实例
document_processor = DocumentProcessor()
