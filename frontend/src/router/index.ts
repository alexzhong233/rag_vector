import { createRouter, createWebHistory } from 'vue-router';
import DocumentsView from '@/views/DocumentsView.vue';
import RagView from '@/views/RagView.vue';
import SettingsView from '@/views/SettingsView.vue';

const routes = [
  {
    path: '/',
    redirect: '/documents',
  },
  {
    path: '/documents',
    name: 'documents',
    component: DocumentsView,
  },
  {
    path: '/rag',
    name: 'rag',
    component: RagView,
  },
  {
    path: '/settings',
    name: 'settings',
    component: SettingsView,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
