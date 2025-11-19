<template>
  <div
    :class="['skeleton', `skeleton--${variant}`, { 'skeleton--rounded': rounded, 'skeleton--circle': circle }]"
    :style="{ width: computedWidth, height: computedHeight }"
  ></div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

interface Props {
  variant?: 'text' | 'rectangular' | 'circular'
  width?: string | number
  height?: string | number
  rounded?: boolean
  circle?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  variant: 'text',
  rounded: false,
  circle: false
})

const computedWidth = computed(() => {
  if (typeof props.width === 'number') {
    return `${props.width}px`
  }
  return props.width || '100%'
})

const computedHeight = computed(() => {
  if (typeof props.height === 'number') {
    return `${props.height}px`
  }
  return props.height || (props.variant === 'text' ? '1rem' : '100%')
})
</script>

<style scoped>
.skeleton {
  background: linear-gradient(
    90deg,
    var(--border-light) 0%,
    var(--background) 50%,
    var(--border-light) 100%
  );
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: var(--radius-sm);
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.skeleton--text {
  height: 1rem;
  margin-bottom: var(--spacing-xs);
  border-radius: var(--radius-sm);
}

.skeleton--rectangular {
  border-radius: var(--radius-md);
}

.skeleton--circular {
  border-radius: 50%;
}

.skeleton--rounded {
  border-radius: var(--radius-lg);
}

.skeleton--circle {
  border-radius: 50%;
  aspect-ratio: 1;
}
</style>
