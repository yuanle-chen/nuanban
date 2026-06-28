<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-blue-500 to-cyan-500 text-white p-6 pt-10 pb-16 rounded-b-3xl">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-blue-100 text-sm">下午好</p>
          <h1 class="text-2xl font-bold mt-1">{{ userStore.userInfo?.username  }} 👋</h1>
        </div>
        <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
          👨
        </div>
      </div>
    </div>

    <!-- 老人状态卡片 -->
    <div class="px-4 -mt-8">
      <div class="bg-white rounded-2xl p-5 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-800">{{ elderName }}</h2>
          <span class="text-green-500 text-sm font-medium flex items-center gap-1">
            <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            在家中
          </span>
        </div>
        <div class="grid grid-cols-3 gap-4 text-center">
          <div>
            <p class="text-2xl font-bold text-green-500">{{ healthSummary.latest_blood_pressure || '--' }}</p>
            <p class="text-xs text-gray-500 mt-1">血压</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-blue-500">{{ healthSummary.latest_heart_rate || '--' }}</p>
            <p class="text-xs text-gray-500 mt-1">心率</p>
          </div>
          <div>
            <p class="text-2xl font-bold text-orange-500">{{ medicationProgress }}</p>
            <p class="text-xs text-gray-500 mt-1">用药情况</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷功能 -->
    <div class="px-4 mt-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">快捷操作</h2>
      <div class="grid grid-cols-4 gap-4">
        <div
          v-for="item in features"
          :key="item.name"
          @click="goTo(item.path)"
          class="bg-white rounded-xl p-4 shadow-sm hover:shadow-md transition-all cursor-pointer text-center"
        >
          <div class="text-3xl mb-2">{{ item.icon }}</div>
          <p class="text-xs text-gray-600">{{ item.name }}</p>
        </div>
      </div>
    </div>

    <!-- 最近提醒 -->
    <div class="px-4 mt-6">
      <div class="flex items-center justify-between mb-4">
        <h2 class="text-lg font-semibold text-gray-800">最近提醒</h2>
        <button @click="goTo('/child/alerts')" class="text-sm text-blue-500">查看全部</button>
      </div>
      <div class="bg-white rounded-2xl shadow-md divide-y divide-gray-100">
        <div
          v-for="alert in alerts"
          :key="alert.time + alert.title"
          class="p-4 flex items-center gap-3"
        >
          <div class="w-10 h-10 rounded-full flex items-center justify-center text-xl" :class="getAlertBgClass(alert.type)">
            {{ alert.icon }}
          </div>
          <div class="flex-1">
            <p class="font-medium text-gray-800">{{ alert.title }}</p>
            <p class="text-xs text-gray-400">今天 {{ alert.time }}</p>
          </div>
        </div>
        <div v-if="alerts.length === 0" class="p-8 text-center text-gray-400">
          <p class="text-3xl mb-2">📭</p>
          <p>暂无提醒</p>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-6 py-3 flex justify-around">
      <div class="text-blue-500 text-center">
        <div class="text-2xl">🏠</div>
        <p class="text-xs mt-1">首页</p>
      </div>
      <div @click="goTo('/child/status')" class="text-gray-400 text-center cursor-pointer">
        <div class="text-2xl">📍</div>
        <p class="text-xs mt-1">状态</p>
      </div>
      <div @click="goTo('/child/alerts')" class="text-gray-400 text-center cursor-pointer">
        <div class="text-2xl">🔔</div>
        <p class="text-xs mt-1">提醒</p>
      </div>
      <div @click="goTo('/child/settings')" class="text-gray-400 text-center cursor-pointer">
        <div class="text-2xl">⚙️</div>
        <p class="text-xs mt-1">设置</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { useFamilyStore } from '../../stores/family'
import { getElderAlerts } from '../../api/family'
import { getHealthSummary } from '../../api/health'
import { getTodayMedication } from '../../api/medication'

const router = useRouter()
const userStore = useUserStore()
const familyStore = useFamilyStore()

const alerts = ref<any[]>([])
const healthSummary = ref<any>({})
const medicationToday = ref<any[]>([])

const elderName = computed(() => {
  const elder = familyStore.currentElder
  if (!elder) return '加载中...'
  return elder.profile?.real_name || elder.username || '老人'
})

const elderId = computed(() => familyStore.currentElder?.id)

const medicationProgress = computed(() => {
  const total = medicationToday.value.length
  const taken = medicationToday.value.filter((m: any) => m.status === 'taken').length
  return total > 0 ? `${taken}/${total}` : '--'
})

const features = [
  { name: '实时状态', icon: '📍', path: '/child/status' },
  { name: '健康报告', icon: '📊', path: '/child/report' },
  { name: '视频通话', icon: '📹', path: '/child' },
  { name: '用药设置', icon: '💊', path: '/child/medication' },
]

function goTo(path: string) {
  router.push(path)
}

function getAlertBgClass(type: string) {
  return type === 'medication' ? 'bg-orange-100' : 'bg-green-100'
}

async function loadData() {
  if (!elderId.value) return
  try {
    const [alertsRes, healthRes, medRes] = await Promise.all([
      getElderAlerts(elderId.value),
      getHealthSummary(elderId.value),
      getTodayMedication(elderId.value)
    ])
    alerts.value = alertsRes
    healthSummary.value = healthRes
    medicationToday.value = medRes
  } catch (error) {
    console.error('加载数据失败', error)
  }
}

onMounted(async () => {
  if (!familyStore.currentElder) {
    await familyStore.fetchElders()
  }
  loadData()
})
</script>