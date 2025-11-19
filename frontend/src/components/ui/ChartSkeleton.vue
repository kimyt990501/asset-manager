<template>
  <div class="chart-skeleton">
    <div class="chart-header">
      <BaseSkeleton width="150px" height="1.25rem" />
      <BaseSkeleton width="80px" height="1rem" />
    </div>
    <div class="chart-body">
      <!-- 막대 그래프 모양 -->
      <div class="chart-bars">
        <div
          v-for="i in barCount"
          :key="i"
          class="chart-bar"
          :style="{ height: getRandomHeight() }"
        >
          <BaseSkeleton width="100%" height="100%" />
        </div>
      </div>
      <!-- X축 레이블 -->
      <div class="chart-labels">
        <BaseSkeleton
          v-for="i in barCount"
          :key="i"
          width="40px"
          height="0.75rem"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import BaseSkeleton from './BaseSkeleton.vue'

interface Props {
  barCount?: number
}

withDefaults(defineProps<Props>(), {
  barCount: 6
})

const getRandomHeight = () => {
  // 랜덤한 높이로 더 자연스러운 스켈레톤
  const heights = ['40%', '60%', '80%', '50%', '70%', '90%']
  return heights[Math.floor(Math.random() * heights.length)]
}
</script>

<style scoped>
.chart-skeleton {
  padding: var(--spacing-lg);
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.chart-body {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.chart-bars {
  display: flex;
  align-items: flex-end;
  gap: var(--spacing-sm);
  height: 200px;
}

.chart-bar {
  flex: 1;
  min-height: 40%;
  border-radius: var(--radius-sm) var(--radius-sm) 0 0;
}

.chart-labels {
  display: flex;
  justify-content: space-around;
  gap: var(--spacing-sm);
}
</style>
