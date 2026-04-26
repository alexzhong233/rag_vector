import axios from 'axios';
import type { Document, DocumentChunk, RagQuery, RagResponse, ChatMessage, SystemConfig } from '@/types';

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export const documentsApi = {
  getAll: (): Promise<Document[]> => {
    return api.get('/documents');
  },
  upload: (formData: FormData, onProgress?: (progress: number) => void): Promise<Document> => {
    return api.post('/documents/upload', formData, {
      onUploadProgress: (progressEvent) => {
        if (progressEvent.total && onProgress) {
          const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          onProgress(progress);
        }
      },
    });
  },
  delete: (id: string): Promise<void> => {
    return api.delete(`/documents/${id}`);
  },
  getChunks: (id: string): Promise<DocumentChunk[]> => {
    return api.get(`/documents/${id}/chunks`);
  },
};

export const ragApi = {
  query: (query: RagQuery): Promise<RagResponse> => {
    return api.post('/rag/query', query);
  },
  getHistory: (): Promise<ChatMessage[]> => {
    return api.get('/rag/history');
  },
};

export const configApi = {
  get: (): Promise<SystemConfig> => {
    return api.get('/config');
  },
  update: (config: SystemConfig): Promise<SystemConfig> => {
    return api.put('/config', config);
  },
};

export default api;
