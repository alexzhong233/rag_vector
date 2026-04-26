<script setup lang="ts">
import { ref } from 'vue';
import { Upload, File, X } from 'lucide-vue-next';

interface Props {
  onUpload?: (file: File, progress: number) => void;
}

const emit = defineEmits<{
  upload: [file: File];
}>();

const isDragging = ref(false);
const selectedFile = ref<File | null>(null);
const uploadProgress = ref(0);
const isUploading = ref(false);

const handleDragOver = (e: DragEvent) => {
  e.preventDefault();
  isDragging.value = true;
};

const handleDragLeave = () => {
  isDragging.value = false;
};

const handleDrop = (e: DragEvent) => {
  e.preventDefault();
  isDragging.value = false;
  const files = e.dataTransfer?.files;
  if (files && files.length > 0) {
    selectedFile.value = files[0];
  }
};

const handleFileSelect = (e: Event) => {
  const target = e.target as HTMLInputElement;
  const files = target.files;
  if (files && files.length > 0) {
    selectedFile.value = files[0];
  }
};

const clearFile = () => {
  selectedFile.value = null;
  uploadProgress.value = 0;
  isUploading.value = false;
};

const handleUpload = () => {
  if (selectedFile.value) {
    emit('upload', selectedFile.value);
  }
};

const formatFileSize = (bytes: number): string => {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(2))} ${sizes[i]}`;
};
</script>

<template>
  <div class="card p-8">
    <div
      :class="[
        'border-2 border-dashed rounded-2xl p-8 text-center transition-all duration-300 cursor-pointer',
        isDragging ? 'border-secondary bg-secondary/5' : 'border-gray-200 hover:border-secondary/50 hover:bg-gray-50',
      ]"
      @dragover="handleDragOver"
      @dragleave="handleDragLeave"
      @drop="handleDrop"
      @click="$refs.fileInput?.click()"
    >
      <input ref="fileInput" type="file" class="hidden" @change="handleFileSelect" />
      
      <div v-if="!selectedFile">
        <div class="w-16 h-16 bg-gradient-to-br from-primary/10 to-secondary/10 rounded-full flex items-center justify-center mx-auto mb-4">
          <Upload class="w-8 h-8 text-primary" />
        </div>
        <h3 class="text-lg font-semibold text-gray-800 mb-2">上传文档</h3>
        <p class="text-gray-500 mb-4">拖拽文件到此处，或点击选择</p>
        <p class="text-sm text-gray-400">支持 PDF、TXT、MD、DOCX 等格式</p>
      </div>

      <div v-else class="flex items-center justify-center gap-4">
        <div class="w-12 h-12 bg-gradient-to-br from-primary to-secondary rounded-xl flex items-center justify-center flex-shrink-0">
          <File class="w-6 h-6 text-white" />
        </div>
        <div class="text-left flex-1 max-w-xs">
          <p class="font-medium text-gray-800 truncate">{{ selectedFile.name }}</p>
          <p class="text-sm text-gray-500">{{ formatFileSize(selectedFile.size) }}</p>
          <div v-if="isUploading" class="mt-3">
            <div class="w-full bg-gray-200 rounded-full h-2">
              <div
                class="bg-gradient-to-r from-primary to-secondary h-2 rounded-full transition-all duration-300"
                :style="{ width: `${uploadProgress}%` }"
              ></div>
            </div>
            <p class="text-sm text-gray-500 mt-1">{{ uploadProgress }}%</p>
          </div>
        </div>
        <button
          @click.stop="clearFile"
          class="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-all"
        >
          <X class="w-5 h-5" />
        </button>
      </div>
    </div>

    <div v-if="selectedFile && !isUploading" class="mt-4 flex justify-end">
      <button @click="handleUpload" class="btn-primary">
        <Upload class="w-5 h-5 inline mr-2" />
        开始上传
      </button>
    </div>
  </div>
</template>
