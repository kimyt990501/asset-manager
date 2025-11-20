<template>
  <div class="chart-container">
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'
import { Bar } from 'vue-chartjs'

ChartJS.register(CategoryScale, LinearScale, BarElement, Title, Tooltip, Legend)

const props = defineProps({
  income: { type: Number, default: 0 },
  fixedExpenses: { type: Number, default: 0 },
  variableExpenses: { type: Number, default: 0 }
})

// CSS 변수에서 색상 가져오기
const getCSSVariable = (variable: string) => {
  return getComputedStyle(document.documentElement).getPropertyValue(variable).trim()
}

const chartData = computed(() => ({
  labels: ['수입', '고정지출', '변동지출', '저축액'],
  datasets: [
    {
      label: '금액',
      backgroundColor: [
        getCSSVariable('--secondary'),      // 수입: 초록
        getCSSVariable('--danger'),         // 고정지출: 빨강
        getCSSVariable('--warning'),        // 변동지출: 주황
        '#6366f1'                           // 저축액: Indigo (Visible in Dark Mode)
      ],
      data: [
        props.income,
        props.fixedExpenses,
        props.variableExpenses,
        props.income - (props.fixedExpenses + props.variableExpenses)
      ],
      borderRadius: 6
    }
  ]
}))

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      grid: {
        color: getCSSVariable('--border-light')
      }
    },
    x: {
      grid: {
        display: false
      }
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>
