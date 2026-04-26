export interface Document {
  id: string;
  name: string;
  type: string;
  size: number;
  status: 'uploading' | 'processing' | 'completed' | 'failed';
  chunkCount: number;
  createdAt: string;
  updatedAt: string;
}

export interface DocumentChunk {
  id: string;
  documentId: string;
  content: string;
  metadata: Record<string, any>;
  embedding?: number[];
  similarity?: number;
}

export interface RagQuery {
  question: string;
  topK: number;
  similarityThreshold: number;
}

export interface RagResponse {
  answer: string;
  sources: DocumentChunk[];
  processingTime: number;
}

export interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: DocumentChunk[];
  timestamp: string;
}

export interface SystemConfig {
  embeddingModel: string;
  llmModel: string;
  chunkSize: number;
  chunkOverlap: number;
  temperature: number;
}
