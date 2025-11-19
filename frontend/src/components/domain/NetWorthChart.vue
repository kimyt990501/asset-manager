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

const chartData = computed(() => ({
  labels: props.labels.length ? props.labels : ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: '순자산',
      backgroundColor: 'rgba(79, 70, 229, 0.1)',
      borderColor: '#4F46E5',
      pointBackgroundColor: '#4F46E5',
      pointBorderColor: '#fff',
      pointHoverBackgroundColor: '#fff',
      pointHoverBorderColor: '#4F46E5',
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
        color: '#E5E7EB'
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
