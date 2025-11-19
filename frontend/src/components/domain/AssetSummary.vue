<template>
  <div class="summary-grid">
    <BaseCard class="summary-card card-animate" style="animation-delay: 0s">
      <div class="card-label">총 자산</div>
      <div class="card-value text-primary">{{ formatCurrency(animatedAssets) }}</div>
    </BaseCard>

    <BaseCard class="summary-card card-animate" style="animation-delay: 0.1s">
      <div class="card-label">부채</div>
      <div class="card-value text-danger">{{ formatCurrency(animatedLiabilities) }}</div>
    </BaseCard>

    <BaseCard class="summary-card card-animate" style="animation-delay: 0.2s">
      <div class="card-label">순자산</div>
      <div class="card-value text-success">{{ formatCurrency(animatedNetWorth) }}</div>
    </BaseCard>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import BaseCard from '../ui/BaseCard.vue'
import { useCountAnimation } from '@/composables/useCountAnimation'

const props = defineProps({
  assets: { type: Number, default: 0 },
  liabilities: { type: Number, default: 0 }
})

const { displayValue: animatedAssets } = useCountAnimation(props.assets, { duration: 1200 })
const { displayValue: animatedLiabilities } = useCountAnimation(props.liabilities, { duration: 1200 })

const netWorth = computed(() => props.assets - props.liabilities)
const { displayValue: animatedNetWorth } = useCountAnimation(netWorth.value, { duration: 1200 })

const formatCurrency = (value: number) => {
  return new Intl.NumberFormat('ko-KR', { style: 'currency', currency: 'KRW' }).format(value)
}
</script>

<style scoped>
.summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-lg);
}

.summary-card {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.card-label {
  font-size: 0.875rem;
  color: var(--text-muted);
  font-weight: 500;
}

.card-value {
  font-size: 1.5rem;
  font-weight: 700;
}

.text-primary { color: var(--primary); }
.text-danger { color: var(--danger); }
.text-success { color: var(--secondary); }

.card-animate {
  animation: slideUpFade 0.6s ease-out both;
}

@keyframes slideUpFade {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
