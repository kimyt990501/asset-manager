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
      backgroundColor: 'rgba(99, 102, 241, 0.1)', /* Indigo with opacity */
      borderColor: '#6366f1', /* Indigo */
      pointBackgroundColor: '#ffffff', /* White dots */
      pointBorderColor: '#6366f1', /* Indigo border */
      pointHoverBackgroundColor: '#ffffff',
      pointHoverBorderColor: '#6366f1',
      fill: true,
      tension: 0.4,
      data: props.dataPoints.length ? props.dataPoints : [0, 0, 0, 0, 0, 0]
    }
  ]
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(24, 24, 27, 0.9)',
      titleColor: '#fff',
      bodyColor: '#fff',
      padding: 12,
      cornerRadius: 8,
      displayColors: false
    }
  },
  scales: {
    y: {
      beginAtZero: false,
      grid: {
        color: 'rgba(0, 0, 0, 0.05)',
        drawBorder: false
      },
      ticks: {
        font: {
          family: "'Inter', sans-serif",
          size: 11
        },
        color: '#71717a'
      }
    },
    x: {
      grid: {
        display: false
      },
      ticks: {
        font: {
          family: "'Inter', sans-serif",
          size: 11
        },
        color: '#71717a'
      }
    }
  },
  elements: {
    line: {
      tension: 0.4,
      borderWidth: 3
    },
    point: {
      radius: 4, /* Visible dots */
      hoverRadius: 6,
      backgroundColor: '#ffffff',
      borderWidth: 2,
      borderColor: '#6366f1' /* Accent color border */
    }
  },
  interaction: {
    intersect: false,
    mode: 'index' as const
  }
}))
</script>

<style scoped>
.chart-container {
  position: relative;
  height: 300px;
  width: 100%;
}
</style>
