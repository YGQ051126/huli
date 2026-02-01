<template>
  <div style="padding:16px">
    <div ref="chartRef" style="height:300px"></div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
const chartRef = ref<HTMLDivElement | null>(null)
onMounted(() => {
  if (!chartRef.value) return
  const chart = echarts.init(chartRef.value)
  chart.setOption({
    tooltip: {},
    xAxis: { type: 'category', data: ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'] },
    yAxis: { type: 'value' },
    series: [{ type: 'bar', data: [12, 20, 15, 8, 10, 18, 22] }]
  })
})
</script>
