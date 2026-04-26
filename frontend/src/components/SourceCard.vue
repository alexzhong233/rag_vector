<script setup lang="ts">
import { FileText, Link } from 'lucide-vue-next';
import type { DocumentChunk } from '@/types';

interface Props {
  source: DocumentChunk;
}

const props = defineProps<Props>();

const formatSimilarity = (similarity?: number): string => {
  if (!similarity) return '';
  return `${Math.round(similarity * 100)}%`;
};
</script>

<template>
  <div class="bg-gray-50 rounded-xl p-4 border border-gray-100">
    <div class="flex items-start justify-between mb-2">
      <div class="flex items-center gap-2">
        <FileText class="w-4 h-4 text-primary" />
        <span class="text-sm font-medium text-gray-700">文档片段</span>
      </div>
      <div v-if="source.similarity" class="flex items-center gap-1">
        <Link class="w-3 h-3 text-secondary" />
        <span class="text-xs font-medium text-secondary">{{ formatSimilarity(source.similarity) }} 匹配</span>
      </div>
    </div>
    <p class="text-sm text-gray-600 line-clamp-3">{{ source.content }}</p>
  </div>
</template>
