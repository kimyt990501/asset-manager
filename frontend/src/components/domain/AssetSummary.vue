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
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-lg);
  margin-bottom: var(--spacing-xl);
}

.summary-card {
  background: var(--surface); /* Explicit White */
  border-radius: var(--radius-xl);
  padding: var(--spacing-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border);
  transition: var(--transition-base);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 160px;
}

.summary-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-md);
  border-color: var(--border-dark);
}

.card-label {
  font-size: 0.95rem;
  color: var(--text-muted);
  font-weight: 600;
  letter-spacing: 0.01em;
  text-transform: uppercase;
}

.card-value {
  font-size: 2rem;
  font-weight: 800;
  letter-spacing: -0.02em;
  line-height: 1.2;
}

.text-primary { 
  color: var(--text-main);
}

.text-danger { 
  color: var(--danger);
}

.text-success { 
  background: linear-gradient(135deg, var(--secondary) 0%, var(--secondary-hover) 100%);
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
}

.card-animate {
  animation: slideUpFade 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) both;
}

@keyframes slideUpFade {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
