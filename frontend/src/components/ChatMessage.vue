<script setup lang="ts">
import { User, Bot } from 'lucide-vue-next';
import type { ChatMessage } from '@/types';
import SourceCard from './SourceCard.vue';

interface Props {
  message: ChatMessage;
}

const props = defineProps<Props>();

const formatTime = (timestamp: string): string => {
  return new Date(timestamp).toLocaleTimeString('zh-CN', {
    hour: '2-digit',
    minute: '2-digit',
  });
};
</script>

<template>
  <div :class="[
    'flex gap-4 mb-6 animate-fade-in',
    message.role === 'user' ? 'flex-row-reverse' : 'flex-row',
  ]">
    <div :class="[
      'w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0',
      message.role === 'user' 
        ? 'bg-gradient-to-br from-primary to-secondary' 
        : 'bg-gray-100',
    ]">
      <User v-if="message.role === 'user'" class="w-5 h-5 text-white" />
      <Bot v-else class="w-5 h-5 text-primary" />
    </div>
    <div :class="[
      'max-w-3xl',
      message.role === 'user' ? 'text-right' : 'text-left',
    ]">
      <div :class="[
        'px-6 py-4 rounded-2xl shadow-sm',
        message.role === 'user'
          ? 'bg-gradient-to-br from-primary to-secondary text-white rounded-tr-sm'
          : 'bg-white rounded-tl-sm',
      ]">
        <p :class="message.role === 'user' ? 'text-white' : 'text-gray-800'">
          {{ message.content }}
        </p>
      </div>
      <p class="text-xs text-gray-400 mt-2 px-1">{{ formatTime(message.timestamp) }}</p>
      
      <div v-if="message.sources && message.sources.length > 0" class="mt-4 space-y-3">
        <p class="text-sm font-medium text-gray-600 px-1">参考来源:</p>
        <SourceCard 
          v-for="(source, index) in message.sources" 
          :key="source.id || index" 
          :source="source" 
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
.animate-fade-in {
  animation: fade-in 0.3s ease-out;
}
</style>
