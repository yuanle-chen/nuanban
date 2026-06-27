<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-blue-500 to-cyan-500 text-white p-6 pt-10 pb-16 rounded-b-3xl">
      <div class="flex items-center justify-between">
        <div>
          <h1 class="text-xl font-bold">实时状态</h1>
          <p class="text-blue-100 text-sm mt-1">{{ elderName }}</p>
        </div>
        <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
          👵
        </div>
      </div>
    </div>

    <!-- 紧急状态卡片 -->
    <div class="px-4 -mt-8">
      <div v-if="hasEmergency" class="bg-gradient-to-r from-red-500 to-orange-500 rounded-2xl p-5 shadow-md text-white">
        <div class="flex items-center gap-3 mb-3">
          <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center animate-pulse">
            🆘
          </div>
          <div>
            <h2 class="font-bold text-lg">紧急求助</h2>
            <p class="text-red-100 text-sm">老人发起了SOS求助！</p>
          </div>
        </div>
        <button
          @click="goTo('/child/alerts')"
          class="w-full py-3 bg-white/20 rounded-xl font-medium"
        >
          立即处理
        </button>
      </div>

      <div v-else class="bg-white rounded-2xl p-5 shadow-md">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-green-100 rounded-full flex items-center justify-center">
            ✅
          </div>
          <div>
            <h2 class="font-semibold text-gray-800">状态正常</h2>
            <p class="text-gray-500 text-sm">老人目前安全，无紧急情况</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 健康数据卡片 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-2xl shadow-md overflow-hidden">
        <div class="p-4 border-b border-gray-100 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-800">健康数据</h2>
          <span class="text-sm text-gray-400">{{ lastUpdateTime }}</span>
        </div>
        <div class="grid grid-cols-2 gap-4 p-4">
          <!-- 血压 -->
          <div class="bg-red-50 rounded-xl p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">血压</span>
              <span class="text-xl">🩺</span>
            </div>
            <p class="text-2xl font-bold" :class="healthStatus.bloodPressure ? 'text-red-500' : 'text-gray-800'">
              {{ healthData.bloodPressure || '--' }}
            </p>
            <p class="text-xs text-gray-400 mt-1">mmHg</p>
          </div>
          <!-- 心率 -->
          <div class="bg-orange-50 rounded-xl p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">心率</span>
              <span class="text-xl">❤️</span>
            </div>
            <p class="text-2xl font-bold" :class="healthStatus.heartRate ? 'text-orange-500' : 'text-gray-800'">
              {{ healthData.heartRate || '--' }}
            </p>
            <p class="text-xs text-gray-400 mt-1">次/分</p>
          </div>
          <!-- 血糖 -->
          <div class="bg-purple-50 rounded-xl p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">血糖</span>
              <span class="text-xl">🩸</span>
            </div>
            <p class="text-2xl font-bold" :class="healthStatus.bloodSugar ? 'text-purple-500' : 'text-gray-800'">
              {{ healthData.bloodSugar || '--' }}
            </p>
            <p class="text-xs text-gray-400 mt-1">mmol/L</p>
          </div>
          <!-- 体重 -->
          <div class="bg-green-50 rounded-xl p-4">
            <div class="flex items-center justify-between mb-2">
              <span class="text-sm text-gray-600">体重</span>
              <span class="text-xl">⚖️</span>
            </div>
            <p class="text-2xl font-bold text-gray-800">
              {{ healthData.weight || '--' }}
            </p>
            <p class="text-xs text-gray-400 mt-1">kg</p>
          </div>
        </div>
        <div class="p-4 border-t border-gray-100">
          <button
            @click="goTo('/child/report')"
            class="w-full py-2 bg-blue-50 text-blue-500 rounded-xl text-sm"
          >
            查看健康报告详情
          </button>
        </div>
      </div>
    </div>

    <!-- 今日用药情况 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-2xl shadow-md overflow-hidden">
        <div class="p-4 border-b border-gray-100 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-800">今日用药</h2>
          <span class="text-sm text-gray-400">{{ medicationProgress }}</span>
        </div>
        <div class="p-4">
          <div class="flex items-center gap-4 mb-4">
            <div class="flex-1 h-3 bg-gray-100 rounded-full overflow-hidden">
              <div
                class="h-full bg-gradient-to-r from-blue-500 to-cyan-500 transition-all"
                :style="{ width: medicationPercentage + '%' }"
              ></div>
            </div>
            <span class="text-sm font-medium text-blue-500">{{ medicationPercentage }}%</span>
          </div>
          <div class="space-y-3">
            <div
              v-for="med in medications"
              :key="med.id"
              class="flex items-center gap-3 p-3 bg-gray-50 rounded-xl"
            >
              <div class="w-8 h-8 rounded-full flex items-center justify-center" :class="med.status === 'taken' ? 'bg-green-100' : 'bg-gray-200'">
                {{ med.status === 'taken' ? '✅' : '💊' }}
              </div>
              <div class="flex-1">
                <p class="font-medium text-gray-800">{{ med.medication_name }}</p>
                <p class="text-xs text-gray-400">{{ med.time }} · {{ med.dosage }}</p>
              </div>
              <span v-if="med.status === 'taken'" class="text-xs text-green-500 bg-green-50 px-2 py-1 rounded-full">
                已服用
              </span>
              <span v-else class="text-xs text-orange-500 bg-orange-50 px-2 py-1 rounded-full">
                未服用
              </span>
            </div>
          </div>
          <div v-if="medications.length === 0" class="py-8 text-center text-gray-400">
            <p class="text-3xl mb-2">💊</p>
            <p>今日暂无用药计划</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 位置信息 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-2xl shadow-md overflow-hidden">
        <div class="p-4 border-b border-gray-100 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-800">位置信息</h2>
          <span class="text-sm text-green-500 flex items-center gap-1">
            <span class="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            在家中
          </span>
        </div>
        <div class="p-4">
          <div class="flex items-center gap-3">
            <div class="w-12 h-12 bg-blue-100 rounded-full flex items-center justify-center text-2xl">
              📍
            </div>
            <div>
              <p class="font-medium text-gray-800">当前位置</p>
              <p class="text-sm text-gray-500">{{ elderProfile?.address || '暂无位置信息' }}</p>
            </div>
          </div>
          <div class="mt-3 p-3 bg-gray-50 rounded-xl text-center text-gray-400 text-sm">
            位置功能需要在手机端开启定位服务
          </div>
        </div>
      </div>
    </div>

    <!-- 最近异常提醒 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-2xl shadow-md overflow-hidden">
        <div class="p-4 border-b border-gray-100 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-800">最近异常</h2>
          <button @click="goTo('/child/alerts')" class="text-sm text-blue-500">查看全部</button>
        </div>
        <div v-if="abnormalAlerts.length === 0" class="p-8 text-center text-gray-400">
          <p class="text-3xl mb-2">✨</p>
          <p>暂无异常提醒</p>
        </div>
        <div v-else class="divide-y divide-gray-100">
          <div
            v-for="alert in abnormalAlerts.slice(0, 3)"
            :key="alert.time + alert.title"
            class="p-4 flex items-center gap-3"
          >
            <div class="w-10 h-10 rounded-full flex items-center justify-center text-xl" :class="getAlertBgClass(alert.type)">
              {{ alert.icon }}
            </div>
            <div class="flex-1">
              <p class="font-medium text-gray-800">{{ alert.title }}</p>
              <p class="text-xs text-gray-400">{{ alert.content }}</p>
            </div>
            <span class="text-xs text-gray-400">{{ alert.time }}</span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useFamilyStore } from '../../stores/family'
import { getHealthSummary } from '../../api/health'
import { getTodayMedication } from '../../api/medication'
import { getPendingEmergencies } from '../../api/emergency'
import { getElderAlerts, getElderProfile } from '../../api/family'

const router = useRouter()
const familyStore = useFamilyStore()

const healthData = ref({
  bloodPressure: '',
  heartRate: '',
  bloodSugar: '',
  weight: ''
})

const healthStatus = ref({
  bloodPressure: false,
  heartRate: false,
  bloodSugar: false
})

const medications = ref<any[]>([])
const emergencies = ref<any[]>([])
const abnormalAlerts = ref<any[]>([])
const elderProfile = ref<any>(null)

const elderName = computed(() => {
  const elder = familyStore.currentElder
  if (!elder) return '加载中...'
  return elder.profile?.real_name || elder.username || '老人'
})

const elderId = computed(() => familyStore.currentElder?.id)

const lastUpdateTime = computed(() => {
  if (healthData.value.bloodPressure || healthData.value.heartRate) {
    return '最近更新'
  }
  return '暂无数据'
})

const hasEmergency = computed(() => emergencies.value.length > 0)

const medicationProgress = computed(() => {
  const total = medications.value.length
  const taken = medications.value.filter((m: any) => m.status === 'taken').length
  return total > 0 ? `${taken}/${total} 已服用` : '暂无计划'
})

const medicationPercentage = computed(() => {
  const total = medications.value.length
  if (total === 0) return 0
  const taken = medications.value.filter((m: any) => m.status === 'taken').length
  return Math.round((taken / total) * 100)
})

function goTo(path: string) {
  router.push(path)
}

function getAlertBgClass(type: string) {
  return type === 'medication' ? 'bg-orange-100' : 'bg-blue-100'
}

async function loadData() {
  if (!elderId.value) return

  try {
    const [healthRes, medRes, emergencyRes, alertsRes, profileRes] = await Promise.all([
      getHealthSummary(elderId.value),
      getTodayMedication(elderId.value),
      getPendingEmergencies(),
      getElderAlerts(elderId.value),
      getElderProfile(elderId.value)
    ])

    // 健康数据
    const health: any = healthRes
    healthData.value = {
      bloodPressure: health.latest_blood_pressure || '',
      heartRate: health.latest_heart_rate || '',
      bloodSugar: health.latest_blood_sugar || '',
      weight: health.latest_weight || ''
    }

    // 健康状态判断
    healthStatus.value = {
      bloodPressure: health.blood_pressure_status === 'abnormal',
      heartRate: health.heart_rate_status === 'abnormal',
      bloodSugar: health.blood_sugar_status === 'abnormal'
    }

    // 用药数据
    medications.value = medRes as any[]

    // 紧急求助
    emergencies.value = emergencyRes as any[]

    // 异常提醒
    abnormalAlerts.value = alertsRes as any[]

    // 老人档案
    elderProfile.value = profileRes
  } catch (error) {
    console.error('加载状态数据失败', error)
  }
}

onMounted(async () => {
  if (!familyStore.currentElder) {
    await familyStore.fetchElders()
  }
  loadData()
})
</script>