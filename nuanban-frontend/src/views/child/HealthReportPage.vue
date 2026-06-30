<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-blue-500 to-cyan-400 text-white p-6 pb-16 rounded-b-3xl">
      <div class="flex items-center gap-3 mb-4">
        <button @click="$router.back()" class="text-white text-lg">← 返回</button>
        <h1 class="text-xl font-bold">健康报告</h1>
      </div>
      <div class="flex items-center gap-3 mt-4">
        <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
          👴
        </div>
        <div>
          <h2 class="text-lg font-bold">{{ elderName }}</h2>
          <p class="text-white/80 text-sm">健康数据汇总</p>
        </div>
      </div>
    </div>

    <!-- 健康状态卡片 -->
    <div class="px-4 -mt-8">
      <div class="bg-white rounded-2xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-800">今日健康状态</h3>
          <span :class="[
            'px-3 py-1 rounded-full text-sm font-medium',
            summary.status === '正常' ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
          ]">
            {{ summary.status }}
          </span>
        </div>
        <div class="grid grid-cols-5 gap-2 text-center">
          <div class="p-3 bg-gray-50 rounded-xl">
            <p class="text-2xl mb-1">🩺</p>
            <p class="text-lg font-bold text-gray-800">{{ summary.latest_blood_pressure || '--' }}</p>
            <p class="text-xs text-gray-500">血压</p>
            <span v-if="summary.latest_blood_pressure" :class="[
              'inline-block mt-1 px-2 py-0.5 rounded-full text-xs',
              checkBloodPressure(summary.latest_blood_pressure) ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
            ]">
              {{ checkBloodPressure(summary.latest_blood_pressure) ? '正常' : '异常' }}
            </span>
          </div>
          <div class="p-3 bg-gray-50 rounded-xl">
            <p class="text-2xl mb-1">❤️</p>
            <p class="text-lg font-bold text-gray-800">{{ summary.latest_heart_rate || '--' }}</p>
            <p class="text-xs text-gray-500">心率</p>
            <span v-if="summary.latest_heart_rate" :class="[
              'inline-block mt-1 px-2 py-0.5 rounded-full text-xs',
              checkHeartRate(summary.latest_heart_rate) ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
            ]">
              {{ checkHeartRate(summary.latest_heart_rate) ? '正常' : '异常' }}
            </span>
          </div>
          <div class="p-3 bg-gray-50 rounded-xl">
            <p class="text-2xl mb-1">🩸</p>
            <p class="text-lg font-bold text-gray-800">{{ summary.latest_blood_sugar || '--' }}</p>
            <p class="text-xs text-gray-500">血糖</p>
            <span v-if="summary.latest_blood_sugar" :class="[
              'inline-block mt-1 px-2 py-0.5 rounded-full text-xs',
              checkBloodSugar(summary.latest_blood_sugar) ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
            ]">
              {{ checkBloodSugar(summary.latest_blood_sugar) ? '正常' : '异常' }}
            </span>
          </div>
          <div class="p-3 bg-gray-50 rounded-xl">
            <p class="text-2xl mb-1">⚖️</p>
            <p class="text-lg font-bold text-gray-800">{{ summary.latest_weight || '--' }}</p>
            <p class="text-xs text-gray-500">体重</p>
          </div>
          <div class="p-3 bg-gray-50 rounded-xl">
            <p class="text-2xl mb-1">😴</p>
            <p class="text-lg font-bold text-gray-800">{{ summary.latest_sleep || '--' }}</p>
            <p class="text-xs text-gray-500">睡眠</p>
            <span v-if="summary.latest_sleep" :class="[
              'inline-block mt-1 px-2 py-0.5 rounded-full text-xs',
              checkSleep(summary.latest_sleep) ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
            ]">
              {{ checkSleep(summary.latest_sleep) ? '正常' : '异常' }}
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 趋势图表 -->
    <div class="px-4 mt-6">
      <div class="bg-white rounded-2xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-800">健康趋势</h3>
          <div class="flex gap-2">
            <button
              v-for="item in chartTypes"
              :key="item.key"
              @click="activeChart = item.key"
              :class="[
                'px-3 py-1 rounded-full text-sm transition-all',
                activeChart === item.key ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-600'
              ]"
            >
              {{ item.name }}
            </button>
          </div>
        </div>
        <div ref="chartRef" class="w-full h-64"></div>
        <div class="mt-4 grid grid-cols-3 gap-3 text-center text-sm">
          <div class="p-3 bg-green-50 rounded-xl">
            <p class="text-gray-500">最高值</p>
            <p class="font-bold text-green-600 text-lg">{{ chartStats.max }}</p>
          </div>
          <div class="p-3 bg-blue-50 rounded-xl">
            <p class="text-gray-500">最低值</p>
            <p class="font-bold text-blue-600 text-lg">{{ chartStats.min }}</p>
          </div>
          <div class="p-3 bg-orange-50 rounded-xl">
            <p class="text-gray-500">平均值</p>
            <p class="font-bold text-orange-600 text-lg">{{ chartStats.avg }}</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 历史记录 -->
    <div class="px-4 mt-6">
      <div class="bg-white rounded-2xl p-6 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h3 class="text-lg font-semibold text-gray-800">历史记录</h3>
          <select
            v-model="filterType"
            @change="loadRecords"
            class="px-3 py-1 border border-gray-200 rounded-lg text-sm focus:outline-none"
          >
            <option value="">全部</option>
            <option value="blood_pressure">血压</option>
            <option value="heart_rate">心率</option>
            <option value="blood_sugar">血糖</option>
            <option value="weight">体重</option>
            <option value="sleep">睡眠</option>
          </select>
        </div>

        <div v-if="records.length === 0" class="text-center text-gray-400 py-8">
          暂无记录
        </div>
        <div v-else class="space-y-2">
          <div
            v-for="record in records"
            :key="record.id"
            class="flex items-center justify-between p-3 bg-gray-50 rounded-xl"
          >
            <div class="flex items-center gap-3">
              <span class="text-xl">{{ getTypeIcon(record.record_type) }}</span>
              <div>
                <p class="font-medium text-gray-800">{{ getTypeName(record.record_type) }}</p>
                <p class="text-xs text-gray-400">{{ formatTime(record.recorded_at) }}</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <span
                v-if="hasStatus(record.record_type)"
                :class="[
                  'px-2 py-0.5 rounded-full text-xs',
                  checkRecordStatus(record.record_type, record.value) ? 'bg-green-100 text-green-600' : 'bg-red-100 text-red-600'
                ]"
              >
                {{ checkRecordStatus(record.record_type, record.value) ? '正常' : '异常' }}
              </span>
              <p class="font-semibold text-blue-600">{{ record.value }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useFamilyStore } from '../../stores/family'
import { getHealthRecords, getHealthSummary } from '../../api/health'
import * as echarts from 'echarts'

const familyStore = useFamilyStore()

const filterType = ref('')
const summary = ref<any>({ status: '正常' })
const records = ref<any[]>([])
const chartRef = ref<HTMLElement | null>(null)
let chartInstance: echarts.ECharts | null = null
const activeChart = ref('heart_rate')
const chartData = ref<any[]>([])

const chartTypes = [
  { key: 'blood_pressure', name: '血压', unit: 'mmHg' },
  { key: 'heart_rate', name: '心率', unit: '次/分' },
  { key: 'blood_sugar', name: '血糖', unit: 'mmol/L' },
  { key: 'weight', name: '体重', unit: 'kg' },
  { key: 'sleep', name: '睡眠', unit: '小时' },
]

const elderName = computed(() => {
  const elder = familyStore.currentElder
  if (!elder) return '加载中...'
  return elder.profile?.real_name || elder.username
})

const elderId = computed(() => familyStore.currentElder?.id)

const currentChartType = computed(() => {
  return chartTypes.find(c => c.key === activeChart.value) || chartTypes[1]
})

const chartStats = computed(() => {
  const data = chartData.value
  if (data.length === 0) return { max: '--', min: '--', avg: '--' }
  
  const values = data.map((d: any) => d.value).filter(v => v !== null && v !== undefined)
  if (values.length === 0) return { max: '--', min: '--', avg: '--' }
  
  const max = Math.max(...values)
  const min = Math.min(...values)
  const avg = (values.reduce((a, b) => a + b, 0) / values.length).toFixed(1)
  
  return { max, min, avg }
})

let syncTimer: ReturnType<typeof setInterval> | null = null

const recordTypes = [
  { key: 'blood_pressure', name: '血压', icon: '🩺' },
  { key: 'heart_rate', name: '心率', icon: '❤️' },
  { key: 'blood_sugar', name: '血糖', icon: '🩸' },
  { key: 'weight', name: '体重', icon: '⚖️' },
  { key: 'sleep', name: '睡眠', icon: '😴' },
]

function getTypeIcon(type: string) {
  const item = recordTypes.find(t => t.key === type)
  return item?.icon || '📊'
}

function getTypeName(type: string) {
  const item = recordTypes.find(t => t.key === type)
  return item?.name || type
}

function formatTime(time: string) {
  const d = new Date(time)
  return `${d.getMonth() + 1}月${d.getDate()}日 ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}

function checkBloodPressure(value: string): boolean {
  try {
    const parts = value.split('/')
    const high = parseInt(parts[0])
    const low = parseInt(parts[1])
    return high >= 90 && high <= 140 && low >= 60 && low <= 90
  } catch {
    return true
  }
}

function checkHeartRate(value: string): boolean {
  try {
    const rate = parseInt(value)
    return rate >= 60 && rate <= 100
  } catch {
    return true
  }
}

function checkBloodSugar(value: string): boolean {
  try {
    const sugar = parseFloat(value)
    return sugar >= 3.9 && sugar <= 6.1
  } catch {
    return true
  }
}

function checkSleep(value: string): boolean {
  try {
    const hours = parseFloat(value)
    return hours >= 6 && hours <= 10
  } catch {
    return true
  }
}

function hasStatus(type: string): boolean {
  return ['blood_pressure', 'heart_rate', 'blood_sugar', 'sleep'].includes(type)
}

function checkRecordStatus(type: string, value: string): boolean {
  switch (type) {
    case 'blood_pressure':
      return checkBloodPressure(value)
    case 'heart_rate':
      return checkHeartRate(value)
    case 'blood_sugar':
      return checkBloodSugar(value)
    case 'sleep':
      return checkSleep(value)
    default:
      return true
  }
}

async function loadSummary() {
  if (!elderId.value) return
  try {
    const res: any = await getHealthSummary(elderId.value)
    summary.value = res
  } catch (error) {
    console.error('加载汇总失败', error)
  }
}

async function loadRecords() {
  if (!elderId.value) return
  try {
    const res: any = await getHealthRecords(elderId.value, filterType.value || undefined, 20)
    records.value = res
  } catch (error) {
    console.error('加载记录失败', error)
  }
}

async function loadChartData() {
  if (!elderId.value) return
  try {
    const res: any = await getHealthRecords(elderId.value, activeChart.value, 30)
    const sorted = [...res].reverse()
    
    chartData.value = sorted.map((item: any) => {
      let value = null
      if (activeChart.value === 'blood_pressure') {
        const parts = item.value.split('/')
        value = parseFloat(parts[0])
      } else {
        value = parseFloat(item.value)
      }
      return {
        date: item.recorded_at,
        value: isNaN(value) ? null : value
      }
    })
    
    updateChart()
  } catch (error) {
    console.error('加载图表数据失败', error)
  }
}

function initChart() {
  if (!chartRef.value) return
  chartInstance = echarts.init(chartRef.value)
  updateChart()
}

function updateChart() {
  if (!chartInstance) return
  
  const dates = chartData.value.map((d: any) => {
    const date = new Date(d.date)
    return `${date.getMonth() + 1}/${date.getDate()}`
  })
  const values = chartData.value.map((d: any) => d.value)
  
  const color = activeChart.value === 'blood_pressure' ? '#ef4444' :
                activeChart.value === 'heart_rate' ? '#3b82f6' :
                activeChart.value === 'blood_sugar' ? '#f59e0b' :
                activeChart.value === 'weight' ? '#8b5cf6' : '#06b6d4'
  
  const option = {
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const p = params[0]
        return `${p.name}<br/>${currentChartType.value.name}: ${p.value || '--'} ${currentChartType.value.unit}`
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      top: '10%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: dates,
      axisLine: { lineStyle: { color: '#e5e7eb' } },
      axisLabel: { color: '#9ca3af', fontSize: 10 }
    },
    yAxis: {
      type: 'value',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f3f4f6' } },
      axisLabel: { color: '#9ca3af', fontSize: 10 }
    },
    series: [
      {
        data: values,
        type: 'line',
        smooth: true,
        lineStyle: { color, width: 2 },
        itemStyle: { color },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: color + '40' },
              { offset: 1, color: color + '05' }
            ]
          }
        },
        symbol: 'circle',
        symbolSize: 6
      }
    ]
  }
  
  chartInstance.setOption(option)
}

function handleResize() {
  chartInstance?.resize()
}

watch(activeChart, () => {
  loadChartData()
})

onMounted(async () => {
  if (!familyStore.currentElder) {
    await familyStore.fetchElders()
  }
  loadSummary()
  loadRecords()
  
  await nextTick()
  initChart()
  loadChartData()
  
  window.addEventListener('resize', handleResize)
  
  syncTimer = setInterval(() => {
    loadSummary()
    loadRecords()
    loadChartData()
  }, 30000)
})

onUnmounted(() => {
  window.removeEventListener('resize', handleResize)
  if (chartInstance) {
    chartInstance.dispose()
    chartInstance = null
  }
  if (syncTimer) {
    clearInterval(syncTimer)
  }
})
</script>