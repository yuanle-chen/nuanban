<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-green-500 to-teal-400 text-white p-6 pb-16 rounded-b-3xl">
      <div class="flex items-center gap-3 mb-4">
        <button @click="$router.back()" class="text-white text-lg">← 返回</button>
        <h1 class="text-xl font-bold">健康记录</h1>
      </div>
      <p class="text-white/80 text-sm">记录每天的健康数据</p>
    </div>

    <!-- 记录类型选择 -->
    <div class="px-4 -mt-8">
      <div class="bg-white rounded-2xl p-4 shadow-md">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">选择记录类型</h2>
        <div class="grid grid-cols-5 gap-2">
          <button
            v-for="item in recordTypes"
            :key="item.key"
            @click="currentType = item.key"
            :class="[
              'p-3 rounded-xl text-center transition-all',
              currentType === item.key ? 'bg-green-100 text-green-600 ring-2 ring-green-400' : 'bg-gray-50 text-gray-600'
            ]"
          >
            <div class="text-2xl mb-1">{{ item.icon }}</div>
            <div class="text-xs">{{ item.name }}</div>
          </button>
        </div>
      </div>
    </div>

    <!-- 输入区域 -->
    <div class="px-4 mt-6">
      <div class="bg-white rounded-2xl p-6 shadow-md">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">
          {{ currentTypeInfo.name }}
        </h3>

        <!-- 血压（特殊：两个值） -->
        <template v-if="currentType === 'blood_pressure'">
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm text-gray-600 mb-1">收缩压（高压）</label>
              <input
                v-model.number="bpHigh"
                type="number"
                placeholder="如 120"
                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-300"
              />
              <p class="text-xs text-gray-400 mt-1">mmHg</p>
            </div>
            <div>
              <label class="block text-sm text-gray-600 mb-1">舒张压（低压）</label>
              <input
                v-model.number="bpLow"
                type="number"
                placeholder="如 80"
                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-300"
              />
              <p class="text-xs text-gray-400 mt-1">mmHg</p>
            </div>
          </div>
        </template>

        <!-- 其他类型（单个值） -->
        <template v-else>
          <div>
            <label class="block text-sm text-gray-600 mb-1">{{ currentTypeInfo.name }}</label>
            <input
              v-model="singleValue"
              :type="currentType === 'sleep' ? 'number' : 'text'"
              :placeholder="currentTypeInfo.placeholder"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-300"
            />
            <p class="text-xs text-gray-400 mt-1">{{ currentTypeInfo.unit }}</p>
          </div>
        </template>

        <button
          @click="handleSubmit"
          :disabled="loading"
          class="w-full mt-6 py-3 bg-gradient-to-r from-green-500 to-teal-400 text-white font-semibold rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
        >
          {{ loading ? '提交中...' : '保存记录' }}
        </button>
      </div>
    </div>

    <!-- 最近记录 -->
    <div class="px-4 mt-6">
      <div class="bg-white rounded-2xl p-6 shadow-md">
        <h3 class="text-lg font-semibold text-gray-800 mb-4">最近记录</h3>
        <div v-if="records.length === 0" class="text-center text-gray-400 py-8">
          暂无记录
        </div>
        <div v-else class="space-y-3">
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
            <p class="font-semibold text-green-600">{{ record.value }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { addHealthRecord, getHealthRecords } from '../../api/health'

const userStore = useUserStore()

const recordTypes = [
  { key: 'blood_pressure', name: '血压', icon: '🩺' },
  { key: 'heart_rate', name: '心率', icon: '❤️' },
  { key: 'blood_sugar', name: '血糖', icon: '🩸' },
  { key: 'weight', name: '体重', icon: '⚖️' },
  { key: 'sleep', name: '睡眠', icon: '😴' },
]

const currentType = ref('blood_pressure')
const bpHigh = ref<number | ''>('')
const bpLow = ref<number | ''>('')
const singleValue = ref('')
const loading = ref(false)
const records = ref<any[]>([])

const currentTypeInfo = computed(() => {
  const info: Record<string, any> = {
    blood_pressure: { name: '血压', unit: 'mmHg', placeholder: '' },
    heart_rate: { name: '心率', unit: '次/分钟', placeholder: '如 75' },
    blood_sugar: { name: '血糖', unit: 'mmol/L', placeholder: '如 5.6' },
    weight: { name: '体重', unit: 'kg', placeholder: '如 65' },
    sleep: { name: '睡眠', unit: '小时', placeholder: '如 8' },
  }
  return info[currentType.value] || {}
})

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
  return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}

async function loadRecords() {
  if (!userStore.userInfo?.id) return
  try {
    const res: any = await getHealthRecords(userStore.userInfo.id, currentType.value, 10)
    records.value = res
  } catch (error) {
    console.error('加载记录失败', error)
  }
}

async function handleSubmit() {
  if (!userStore.userInfo?.id) {
    alert('请先登录')
    return
  }

  let value = ''
  if (currentType.value === 'blood_pressure') {
    if (!bpHigh.value || !bpLow.value) {
      alert('请输入收缩压和舒张压')
      return
    }
    value = `${bpHigh.value}/${bpLow.value}`
  } else {
    if (!singleValue.value) {
      alert('请输入数值')
      return
    }
    value = singleValue.value
  }

  loading.value = true
  try {
    await addHealthRecord(userStore.userInfo.id, currentType.value, value)
    alert('记录成功！')
    if (currentType.value === 'blood_pressure') {
      bpHigh.value = ''
      bpLow.value = ''
    } else {
      singleValue.value = ''
    }
    await loadRecords()
  } catch (err: any) {
    alert(err.response?.data?.detail || '记录失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadRecords()
})
</script>