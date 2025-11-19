<template>
  <div class="empty-state">
    <div class="empty-state-icon">
      <slot name="icon">
        <!-- Default Icon: Empty Box -->
        <svg
          xmlns="http://www.w3.org/2000/svg"
          width="64"
          height="64"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
          stroke-linecap="round"
          stroke-linejoin="round"
        >
          <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
          <polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline>
          <line x1="12" y1="22.08" x2="12" y2="12"></line>
        </svg>
      </slot>
    </div>

    <div class="empty-state-content">
      <h3 class="empty-state-title">{{ title }}</h3>
      <p v-if="description" class="empty-state-description">{{ description }}</p>
    </div>

    <div v-if="$slots.action || action" class="empty-state-action">
      <slot name="action">
        <BaseButton
          v-if="action"
          :variant="actionVariant"
          @click="$emit('action')"
        >
          {{ action }}
        </BaseButton>
      </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseButton from './BaseButton.vue'

interface Props {
  title: string
  description?: string
  action?: string
  actionVariant?: 'primary' | 'secondary' | 'danger' | 'ghost'
}

withDefaults(defineProps<Props>(), {
  actionVariant: 'primary'
})

defineEmits(['action'])
</script>

<style scoped>
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-2xl) var(--spacing-xl);
  text-align: center;
  min-height: 300px;
}

.empty-state-icon {
  color: var(--text-light);
  margin-bottom: var(--spacing-lg);
  animation: fadeInUp 0.5s ease-out;
}

.empty-state-content {
  max-width: 400px;
  animation: fadeInUp 0.5s ease-out 0.1s both;
}

.empty-state-title {
  font-size: var(--font-2xl);
  font-weight: var(--font-bold);
  color: var(--text-main);
  margin-bottom: var(--spacing-sm);
  letter-spacing: -0.02em;
}

.empty-state-description {
  font-size: var(--font-base);
  color: var(--text-muted);
  line-height: var(--leading-relaxed);
  margin-bottom: var(--spacing-lg);
}

.empty-state-action {
  animation: fadeInUp 0.5s ease-out 0.2s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 반응형 */
@media (max-width: 768px) {
  .empty-state {
    padding: var(--spacing-xl) var(--spacing-md);
  }

  .empty-state-title {
    font-size: var(--font-xl);
  }

  .empty-state-description {
    font-size: var(--font-sm);
  }
}
</style>
