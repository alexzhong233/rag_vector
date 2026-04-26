<script setup lang="ts">
import { RouterLink, useRoute } from 'vue-router';
import { FileText, MessageSquare, Settings, Database } from 'lucide-vue-next';

const route = useRoute();

const isActive = (path: string) => {
  return route.path === path;
};
</script>

<template>
  <div class="flex h-screen bg-gray-50">
    <aside class="w-64 bg-white border-r border-gray-200 flex flex-col">
      <div class="p-6 border-b border-gray-100">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center">
            <Database class="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 class="font-bold text-lg text-gray-800">RAG Vector</h1>
            <p class="text-xs text-gray-500">智能知识库系统</p>
          </div>
        </div>
      </div>

      <nav class="flex-1 p-4 space-y-2">
        <RouterLink
          to="/documents"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200',
            isActive('/documents')
              ? 'bg-gradient-to-r from-primary to-secondary text-white shadow-md'
              : 'text-gray-600 hover:bg-gray-50',
          ]"
        >
          <FileText class="w-5 h-5" />
          <span class="font-medium">文档管理</span>
        </RouterLink>

        <RouterLink
          to="/rag"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200',
            isActive('/rag')
              ? 'bg-gradient-to-r from-primary to-secondary text-white shadow-md'
              : 'text-gray-600 hover:bg-gray-50',
          ]"
        >
          <MessageSquare class="w-5 h-5" />
          <span class="font-medium">RAG 问答</span>
        </RouterLink>

        <RouterLink
          to="/settings"
          :class="[
            'flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200',
            isActive('/settings')
              ? 'bg-gradient-to-r from-primary to-secondary text-white shadow-md'
              : 'text-gray-600 hover:bg-gray-50',
          ]"
        >
          <Settings class="w-5 h-5" />
          <span class="font-medium">系统设置</span>
        </RouterLink>
      </nav>

      <div class="p-4 border-t border-gray-100">
        <div class="bg-gray-50 rounded-xl p-4">
          <p class="text-xs text-gray-500 mb-2">当前状态</p>
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span class="text-sm text-gray-700 font-medium">系统运行中</span>
          </div>
        </div>
      </div>
    </aside>

    <main class="flex-1 overflow-hidden">
      <router-view />
    </main>
  </div>
</template>
