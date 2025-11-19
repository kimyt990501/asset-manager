<template>
  <div class="chart-container">
    <Line :data="chartData" :options="chartOptions" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  dataPoints: { type: Array as () => number[], default: () => [] },
  labels: { type: Array as () => string[], default: () => [] }
})

// CSS 변수에서 색상 가져오기
const getCSSVariable = (variable: string) => {
  return getComputedStyle(document.documentElement).getPropertyValue(variable).trim()
}

// 색상을 rgba로 변환 (투명도 적용)
const hexToRgba = (hex: string, alpha: number) => {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha})`
}

const primaryColor = getCSSVariable('--primary')

const chartData = computed(() => ({
  labels: props.labels.length ? props.labels : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: '순자산',
      backgroundColor: hexToRgba(primaryColor, 0.1),
      borderColor: primaryColor,
      pointBackgroundColor: primaryColor,
      pointBorderColor: getCSSVariable('--surface'),
      pointHoverBackgroundColor: getCSSVariable('--surface'),
      pointHoverBorderColor: primaryColor,
      fill: true,
      tension: 0.4,
      data: props.dataPoints.length ? props.dataPoints : [0, 0, 0, 0, 0, 0]
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
