<script setup lang="ts">
import { FileText, Trash2, Clock, CheckCircle, AlertCircle } from 'lucide-vue-next';
import type { Document } from '@/types';

interface Props {
  document: Document;
  onDelete?: (id: string) => void;
}

const props = defineProps<Props>();
const emit = defineEmits<{
  delete: [id: string];
}>();

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};

const formatDate = (dateStr: string): string => {
  return new Date(dateStr).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
};

const getStatusConfig = (status: Document['status']) => {
  switch (status) {
    case 'uploading':
      return { icon: Clock, color: 'text-yellow-500', bg: 'bg-yellow-50', label: '上传中' };
    case 'processing':
      return { icon: Clock, color: 'text-blue-500', bg: 'bg-blue-50', label: '处理中' };
    case 'completed':
      return { icon: CheckCircle, color: 'text-green-500', bg: 'bg-green-50', label: '已完成' };
    case 'failed':
      return { icon: AlertCircle, color: 'text-red-500', bg: 'bg-red-50', label: '失败' };
    default:
      return { icon: Clock, color: 'text-gray-500', bg: 'bg-gray-50', label: '未知' };
  }
};

const statusConfig = getStatusConfig(props.document.status);
const StatusIcon = statusConfig.icon;
</script>

<template>
  <div class="card p-6 hover:border-secondary/30 border-2 border-transparent">
    <div class="flex items-start justify-between">
      <div class="flex items-start gap-4 flex-1">
        <div class="w-12 h-12 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center flex-shrink-0">
          <FileText class="w-6 h-6 text-white" />
        </div>
        <div class="flex-1 min-w-0">
          <h3 class="font-semibold text-lg text-gray-800 truncate">{{ document.name }}</h3>
          <div class="flex items-center gap-4 mt-2 text-sm text-gray-500">
            <span>{{ formatFileSize(document.size) }}</span>
            <span>·</span>
            <span>{{ formatDate(document.createdAt) }}</span>
            <span v-if="document.chunkCount > 0">·</span>
            <span v-if="document.chunkCount > 0">{{ document.chunkCount }} 切片</span>
          </div>
        </div>
      </div>
      <div class="flex items-center gap-3">
        <div class="flex items-center gap-2 px-3 py-1 rounded-full" :class="statusConfig.bg">
          <StatusIcon class="w-4 h-4" :class="statusConfig.color" />
          <span class="text-sm font-medium" :class="statusConfig.color">{{ statusConfig.label }}</span>
        </div>
        <button
          @click="emit('delete', document.id)"
          class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all duration-200"
        >
          <Trash2 class="w-5 h-5" />
        </button>
      </div>
    </div>
  </div>
</template>
