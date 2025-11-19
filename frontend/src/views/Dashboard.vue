<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <div class="header-content">
        <h1>나의 자산 현황</h1>
        <p class="subtitle">반갑습니다. 현재 재무 상태를 한눈에 확인하세요.</p>
      </div>
      <div class="date-selector glass-panel">
        <span>{{ currentDate }}</span>
        <i class="icon-chevron-down"></i>
      </div>
    </header>

    <!-- Asset Summary -->
    <section class="section">
      <AssetSummary 
        :assets="summaryData.assets" 
        :liabilities="summaryData.liabilities" 
      />
    </section>

    <div class="charts-grid">
      <!-- Monthly Overview -->
      <section class="section">
        <BaseCard>
          <div class="card-header">
            <h3 class="card-title">월별 수입/지출</h3>
            <span class="card-badge">수입 vs 지출</span>
          </div>
          <MonthlyChart 
            :income="monthlyData.income"
            :fixedExpenses="monthlyData.fixedExpenses"
            :variableExpenses="monthlyData.variableExpenses"
          />
        </BaseCard>
      </section>

      <!-- Net Worth Trend -->
      <section class="section">
        <BaseCard>
          <div class="card-header">
            <h3 class="card-title">순자산 추이</h3>
            <span class="card-badge">최근 6개월</span>
          </div>
          <NetWorthChart 
            :dataPoints="netWorthTrend.data"
            :labels="netWorthTrend.labels"
          />
        </BaseCard>
      </section>
    </div>
  </div>
</template>


<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { storeToRefs } from 'pinia'
import { useSummaryStore } from '@/stores/summaryStore'
import BaseCard from '../components/ui/BaseCard.vue'
import AssetSummary from '../components/domain/AssetSummary.vue'
import MonthlyChart from '../components/domain/MonthlyChart.vue'
import NetWorthChart from '../components/domain/NetWorthChart.vue'

const summaryStore = useSummaryStore()
const { 
  totalAssets, 
  monthlyFixedIncome, 
  monthlyFixedExpenses, 
  netWorthTrend 
} = storeToRefs(summaryStore)

// Fetch data on mount
onMounted(async () => {
  await Promise.all([
    summaryStore.fetchSummary(),
    summaryStore.fetchTrend()
  ])
})

// Computed props for child components
// Note: Liabilities are not yet tracked separately in the backend summary, 
// so we assume 0 for now or we could add a liabilities field later.
// For now, let's assume totalAssets is Net Worth.
const summaryData = computed(() => ({
  assets: totalAssets.value,
  liabilities: 0 // Placeholder
}))

const monthlyData = computed(() => ({
  income: monthlyFixedIncome.value,
  fixedExpenses: monthlyFixedExpenses.value,
  variableExpenses: 0 // Variable expenses are not yet in the summary endpoint
}))

const currentDate = computed(() => {
  const now = new Date()
  return `${now.getFullYear()}년 ${now.getMonth() + 1}월`
})

</script>

<style scoped>
.dashboard {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xl);
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: var(--spacing-md);
}

.header-content h1 {
  font-size: 2.25rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.03em;
  margin-bottom: 0.25rem;
}

.subtitle {
  color: var(--text-muted);
  font-size: 1rem;
}

.date-selector {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-full);
  font-weight: 600;
  color: var(--text-main);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: var(--transition-base);
}

.date-selector:hover {
  background: var(--surface);
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: var(--spacing-lg);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
  letter-spacing: -0.01em;
}

.card-badge {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--primary);
  background: var(--primary-light);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
}

@media (max-width: 768px) {
  .dashboard-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }
  
  .charts-grid {
    grid-template-columns: 1fr;
  }
}
</style>

