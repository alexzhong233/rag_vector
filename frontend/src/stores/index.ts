import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { Document, ChatMessage, SystemConfig } from '@/types';

export const useDocumentStore = defineStore('documents', () => {
  const documents = ref<Document[]>([]);
  const loading = ref(false);

  const setDocuments = (newDocuments: Document[]) => {
    documents.value = newDocuments;
  };

  const addDocument = (document: Document) => {
    documents.value.unshift(document);
  };

  const removeDocument = (id: string) => {
    documents.value = documents.value.filter(doc => doc.id !== id);
  };

  const updateDocumentStatus = (id: string, status: Document['status']) => {
    const doc = documents.value.find(d => d.id === id);
    if (doc) {
      doc.status = status;
    }
  };

  return {
    documents,
    loading,
    setDocuments,
    addDocument,
    removeDocument,
    updateDocumentStatus,
  };
});

export const useChatStore = defineStore('chat', () => {
  const messages = ref<ChatMessage[]>([]);
  const isTyping = ref(false);

  const addMessage = (message: ChatMessage) => {
    messages.value.push(message);
  };

  const setMessages = (newMessages: ChatMessage[]) => {
    messages.value = newMessages;
  };

  const clearMessages = () => {
    messages.value = [];
  };

  return {
    messages,
    isTyping,
    addMessage,
    setMessages,
    clearMessages,
  };
});

export const useConfigStore = defineStore('config', () => {
  const config = ref<SystemConfig>({
    embeddingModel: 'text-embedding-ada-002',
    llmModel: 'gpt-3.5-turbo',
    chunkSize: 1000,
    chunkOverlap: 200,
    temperature: 0.7,
  });

  const setConfig = (newConfig: SystemConfig) => {
    config.value = newConfig;
  };

  const updateConfig = (updates: Partial<SystemConfig>) => {
    config.value = { ...config.value, ...updates };
  };

  return {
    config,
    setConfig,
    updateConfig,
  };
});
