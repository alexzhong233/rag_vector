<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue';
import { Send, MessageSquare } from 'lucide-vue-next';
import ChatMessage from '@/components/ChatMessage.vue';
import { useChatStore } from '@/stores';
import type { ChatMessage as ChatMessageType } from '@/types';

const chatStore = useChatStore();
const inputValue = ref('');
const messagesContainer = ref<HTMLElement | null>(null);

const mockChatHistory: ChatMessageType[] = [
  {
    id: '1',
    role: 'user',
    content: '什么是人工智能？',
    timestamp: '2024-01-16T10:00:00Z',
  },
  {
    id: '2',
    role: 'assistant',
    content: '人工智能（Artificial Intelligence，简称 AI）是计算机科学的一个分支，它企图了解智能的实质，并生产出一种新的能以人类智能相似的方式做出反应的智能机器。',
    sources: [
      {
        id: 's1',
        documentId: '1',
        content: '人工智能技术白皮书指出，AI 是计算机科学的重要分支...',
        metadata: {},
        similarity: 0.92,
      },
    ],
    timestamp: '2024-01-16T10:00:05Z',
  },
];

onMounted(() => {
  chatStore.setMessages(mockChatHistory);
  scrollToBottom();
});

const scrollToBottom = () => {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
  });
};

const handleSendMessage = async () => {
  if (!inputValue.value.trim()) return;

  const userMessage: ChatMessageType = {
    id: Date.now().toString(),
    role: 'user',
    content: inputValue.value,
    timestamp: new Date().toISOString(),
  };

  chatStore.addMessage(userMessage);
  const question = inputValue.value;
  inputValue.value = '';
  chatStore.isTyping = true;
  scrollToBottom();

  setTimeout(() => {
    const assistantMessage: ChatMessageType = {
      id: (Date.now() + 1).toString(),
      role: 'assistant',
      content: `这是针对您的问题 "${question}" 的模拟回答。在实际应用中，这里会显示 AI 根据您的文档内容生成的响应。`,
      sources: [
        {
          id: 's2',
          documentId: '1',
          content: '这是从文档中检索到的相关片段...',
          metadata: {},
          similarity: 0.85,
        },
      ],
      timestamp: new Date().toISOString(),
    };
    chatStore.addMessage(assistantMessage);
    chatStore.isTyping = false;
    scrollToBottom();
  }, 1500);
};

const handleKeyPress = (e: KeyboardEvent) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    handleSendMessage();
  }
};
</script>

<template>
  <div class="flex flex-col h-screen">
    <div class="border-b border-gray-200 bg-white px-8 py-4">
      <h1 class="text-2xl font-bold text-gray-800">RAG 问答</h1>
      <p class="text-gray-500 text-sm">基于知识库文档进行智能问答</p>
    </div>

    <div
      ref="messagesContainer"
      class="flex-1 overflow-y-auto p-8 bg-gray-50"
    >
      <div class="max-w-4xl mx-auto">
        <div v-if="chatStore.messages.length === 0" class="text-center py-16">
          <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <MessageSquare class="w-12 h-12 text-gray-400" />
          </div>
          <h3 class="text-xl font-medium text-gray-700 mb-2">开始对话</h3>
          <p class="text-gray-500">输入你的问题，AI 将基于知识库为你解答</p>
        </div>

        <div v-else>
          <ChatMessage
            v-for="msg in chatStore.messages"
            :key="msg.id"
            :message="msg"
          />

          <div v-if="chatStore.isTyping" class="flex gap-4 mb-6">
            <div class="w-10 h-10 rounded-xl bg-gray-100 flex items-center justify-center flex-shrink-0">
              <MessageSquare class="w-5 h-5 text-primary" />
            </div>
            <div class="bg-white px-6 py-4 rounded-2xl shadow-sm rounded-tl-sm">
              <div class="flex gap-2">
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 0ms"></div>
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 150ms"></div>
                <div class="w-2 h-2 bg-primary rounded-full animate-bounce" style="animation-delay: 300ms"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="border-t border-gray-200 bg-white p-6">
      <div class="max-w-4xl mx-auto">
        <div class="flex gap-4">
          <textarea
            v-model="inputValue"
            @keydown="handleKeyPress"
            placeholder="输入你的问题..."
            class="input-field flex-1 resize-none"
            rows="1"
          />
          <button
            @click="handleSendMessage"
            :disabled="!inputValue.trim()"
            class="btn-primary disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send class="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
