<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { FileText, Plus } from 'lucide-vue-next';
import DocumentCard from '@/components/DocumentCard.vue';
import DocumentUploader from '@/components/DocumentUploader.vue';
import { useDocumentStore } from '@/stores';
import type { Document } from '@/types';

const documentStore = useDocumentStore();
const showUploader = ref(false);

const mockDocuments: Document[] = [
  {
    id: '1',
    name: '人工智能技术白皮书.pdf',
    type: 'application/pdf',
    size: 2456789,
    status: 'completed',
    chunkCount: 45,
    createdAt: '2024-01-15T10:30:00Z',
    updatedAt: '2024-01-15T10:30:00Z',
  },
  {
    id: '2',
    name: '项目需求说明书.md',
    type: 'text/markdown',
    size: 123456,
    status: 'completed',
    chunkCount: 12,
    createdAt: '2024-01-14T15:20:00Z',
    updatedAt: '2024-01-14T15:20:00Z',
  },
  {
    id: '3',
    name: '技术架构设计文档.docx',
    type: 'application/docx',
    size: 1876543,
    status: 'processing',
    chunkCount: 0,
    createdAt: '2024-01-16T09:15:00Z',
    updatedAt: '2024-01-16T09:15:00Z',
  },
];

onMounted(() => {
  documentStore.setDocuments(mockDocuments);
});

const handleDelete = (id: string) => {
  documentStore.removeDocument(id);
};

const handleUpload = async (file: File) => {
  const newDoc: Document = {
    id: Date.now().toString(),
    name: file.name,
    type: file.type,
    size: file.size,
    status: 'uploading',
    chunkCount: 0,
    createdAt: new Date().toISOString(),
    updatedAt: new Date().toISOString(),
  };
  documentStore.addDocument(newDoc);
  showUploader.value = false;
  
  setTimeout(() => {
    documentStore.updateDocumentStatus(newDoc.id, 'processing');
    setTimeout(() => {
      documentStore.updateDocumentStatus(newDoc.id, 'completed');
      const doc = documentStore.documents.find(d => d.id === newDoc.id);
      if (doc) {
        doc.chunkCount = Math.floor(file.size / 10000) + 5;
      }
    }, 2000);
  }, 1000);
};
</script>

<template>
  <div class="p-8 max-w-7xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 mb-2">文档管理</h1>
        <p class="text-gray-500">管理和上传你的知识库文档</p>
      </div>
      <button 
        @click="showUploader = !showUploader"
        class="btn-primary"
      >
        <Plus class="w-5 h-5 inline mr-2" />
        上传文档
      </button>
    </div>

    <div v-if="showUploader" class="mb-8">
      <DocumentUploader @upload="handleUpload" />
    </div>

    <div v-if="documentStore.documents.length > 0" class="space-y-4">
      <DocumentCard
        v-for="doc in documentStore.documents"
        :key="doc.id"
        :document="doc"
        @delete="handleDelete"
      />
    </div>

    <div v-else class="text-center py-16">
      <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
        <FileText class="w-12 h-12 text-gray-400" />
      </div>
      <h3 class="text-xl font-medium text-gray-700 mb-2">暂无文档</h3>
      <p class="text-gray-500 mb-6">开始上传你的第一个文档到知识库</p>
      <button @click="showUploader = true" class="btn-primary">
        <Plus class="w-5 h-5 inline mr-2" />
        上传文档
      </button>
    </div>
  </div>
</template>
