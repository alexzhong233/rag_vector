<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { Settings, Save } from 'lucide-vue-next';
import { useConfigStore } from '@/stores';
import type { SystemConfig } from '@/types';

const configStore = useConfigStore();
const isSaving = ref(false);
const showSuccess = ref(false);

const formConfig = ref<SystemConfig>({
  embeddingModel: 'text-embedding-ada-002',
  llmModel: 'gpt-3.5-turbo',
  chunkSize: 1000,
  chunkOverlap: 200,
  temperature: 0.7,
});

onMounted(() => {
  formConfig.value = { ...configStore.config };
});

const handleSave = async () => {
  isSaving.value = true;
  
  setTimeout(() => {
    configStore.setConfig({ ...formConfig.value });
    isSaving.value = false;
    showSuccess.value = true;
    
    setTimeout(() => {
      showSuccess.value = false;
    }, 3000);
  }, 1000);
};

const embeddingModels = [
  { value: 'text-embedding-ada-002', label: 'OpenAI text-embedding-ada-002' },
  { value: 'text-embedding-3-small', label: 'OpenAI text-embedding-3-small' },
  { value: 'text-embedding-3-large', label: 'OpenAI text-embedding-3-large' },
];

const llmModels = [
  { value: 'gpt-3.5-turbo', label: 'OpenAI GPT-3.5 Turbo' },
  { value: 'gpt-4', label: 'OpenAI GPT-4' },
  { value: 'gpt-4-turbo', label: 'OpenAI GPT-4 Turbo' },
];
</script>

<template>
  <div class="p-8 max-w-4xl mx-auto">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h1 class="text-3xl font-bold text-gray-800 mb-2">系统设置</h1>
        <p class="text-gray-500">配置向量模型和 RAG 参数</p>
      </div>
      <button @click="handleSave" :disabled="isSaving" class="btn-primary">
        <Save class="w-5 h-5 inline mr-2" />
        {{ isSaving ? '保存中...' : '保存设置' }}
      </button>
    </div>

    <div v-if="showSuccess" class="mb-6 bg-green-50 border border-green-200 text-green-700 px-6 py-4 rounded-xl flex items-center gap-3">
      <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
      </svg>
      <span>设置保存成功！</span>
    </div>

    <div class="space-y-8">
      <div class="card p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-6 flex items-center gap-3">
          <Settings class="w-6 h-6 text-primary" />
          模型配置
        </h2>
        
        <div class="grid md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">Embedding 模型</label>
            <select v-model="formConfig.embeddingModel" class="input-field">
              <option v-for="model in embeddingModels" :key="model.value" :value="model.value">
                {{ model.label }}
              </option>
            </select>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">LLM 模型</label>
            <select v-model="formConfig.llmModel" class="input-field">
              <option v-for="model in llmModels" :key="model.value" :value="model.value">
                {{ model.label }}
              </option>
            </select>
          </div>
        </div>
      </div>

      <div class="card p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-6">文档切片配置</h2>
        
        <div class="grid md:grid-cols-2 gap-6">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              切片大小 (token)
            </label>
            <input
              v-model.number="formConfig.chunkSize"
              type="number"
              min="100"
              max="4000"
              class="input-field"
            />
            <p class="text-xs text-gray-500 mt-1">每个文档切片的 token 数量，建议 500-2000</p>
          </div>
          
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-2">
              重叠大小 (token)
            </label>
            <input
              v-model.number="formConfig.chunkOverlap"
              type="number"
              min="0"
              max="1000"
              class="input-field"
            />
            <p class="text-xs text-gray-500 mt-1">相邻切片之间的重叠 token 数量</p>
          </div>
        </div>
      </div>

      <div class="card p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-6">生成配置</h2>
        
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-2">
            Temperature: {{ formConfig.temperature }}
          </label>
          <input
            v-model.number="formConfig.temperature"
            type="range"
            min="0"
            max="1"
            step="0.1"
            class="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
          />
          <div class="flex justify-between text-xs text-gray-500 mt-1">
            <span>精确</span>
            <span>有创意</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
