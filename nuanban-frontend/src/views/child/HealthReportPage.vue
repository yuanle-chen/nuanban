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
          </div>
          <div class="p-3 bg-gray-50 rounded-xl">
            <p class="text-2xl mb-1">❤️</p>
            <p class="text-lg font-bold text-gray-800">{{ summary.latest_heart_rate || '--' }}</p>
            <p class="text-xs text-gray-500">心率</p>
          </div>
          <div class="p-3 bg-gray-50 rounded-xl">
            <p class="text-2xl mb-1">🩸</p>
            <p class="text-lg font-bold text-gray-800">{{ summary.latest_blood_sugar || '--' }}</p>
            <p class="text-xs text-gray-500">血糖</p>
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
            <p class="font-semibold text-blue-600">{{ record.value }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useFamilyStore } from '../../stores/family'
import { getHealthRecords, getHealthSummary } from '../../api/health'

const familyStore = useFamilyStore()

const filterType = ref('')
const summary = ref<any>({ status: '正常' })
const records = ref<any[]>([])

const elderName = computed(() => {
  const elder = familyStore.currentElder
  if (!elder) return '加载中...'
  return elder.profile?.real_name || elder.username
})

const elderId = computed(() => familyStore.currentElder?.id)

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

onMounted(async () => {
  if (!familyStore.currentElder) {
    await familyStore.fetchElders()
  }
  loadSummary()
  loadRecords()
})
</script>