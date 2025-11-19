<template>
  <Teleport to="body">
    <div class="toast-container">
      <TransitionGroup name="toast-list">
        <BaseToast
          v-for="toast in toasts"
          :key="toast.id"
          :type="toast.type"
          :message="toast.message"
          @close="removeToast(toast.id)"
        />
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { storeToRefs } from 'pinia'
import { useToastStore } from '@/stores/toastStore'
import BaseToast from './BaseToast.vue'

const toastStore = useToastStore()
const { toasts } = storeToRefs(toastStore)
const { removeToast } = toastStore
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: var(--spacing-xl);
  right: var(--spacing-xl);
  z-index: var(--z-toast);
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
  pointer-events: none;
}

.toast-container > * {
  pointer-events: auto;
}

/* TransitionGroup animations */
.toast-list-enter-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.toast-list-leave-active {
  transition: all 0.2s cubic-bezier(0.4, 0, 1, 1);
}

.toast-list-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.toast-list-leave-to {
  opacity: 0;
  transform: translateX(50%) scale(0.8);
}

.toast-list-move {
  transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

/* 모바일 대응 */
@media (max-width: 768px) {
  .toast-container {
    top: var(--spacing-md);
    right: var(--spacing-md);
    left: var(--spacing-md);
  }
}
</style>
