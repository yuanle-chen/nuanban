<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 pb-20">
    <div class="bg-gradient-to-r from-orange-400 to-amber-500 text-white p-6 pt-10 pb-16 rounded-b-3xl">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-orange-100 text-sm">{{ greeting }}</p>
          <h1 class="text-2xl font-bold mt-1">{{ userStore.userInfo?.username }} 👋</h1>
        </div>
        <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
          👵
        </div>
      </div>
    </div>

    <div class="px-4 -mt-8">
      <div class="bg-white rounded-2xl p-5 shadow-md">
        <div class="flex items-center justify-between mb-4">
          <h2 class="text-lg font-semibold text-gray-800">今日健康</h2>
          <span class="text-xs text-gray-400">{{ lastUpdateTime }}</span>
        </div>
        <div class="grid grid-cols-2 gap-4">
          <div :class="['rounded-xl p-4 text-center', healthStatus.bloodPressure ? 'bg-red-50' : 'bg-orange-50']">
            <p :class="['text-2xl font-bold', healthStatus.bloodPressure ? 'text-red-500' : 'text-orange-500']">
              {{ healthData.bloodPressure || '--' }}
            </p>
            <p class="text-sm text-gray-500 mt-1">血压 mmHg</p>
            <span v-if="healthStatus.bloodPressure" class="inline-block mt-1 px-2 py-0.5 bg-red-100 text-red-600 rounded-full text-xs">异常</span>
          </div>
          <div :class="['rounded-xl p-4 text-center', healthStatus.heartRate ? 'bg-red-50' : 'bg-orange-50']">
            <p :class="['text-2xl font-bold', healthStatus.heartRate ? 'text-red-500' : 'text-orange-500']">
              {{ healthData.heartRate || '--' }}
            </p>
            <p class="text-sm text-gray-500 mt-1">心率 次/分</p>
            <span v-if="healthStatus.heartRate" class="inline-block mt-1 px-2 py-0.5 bg-red-100 text-red-600 rounded-full text-xs">异常</span>
          </div>
        </div>
        <div v-if="showNewDayAlert" class="mt-4 p-3 bg-blue-50 rounded-xl text-center">
          <p class="text-blue-600 text-sm">☀️ 新的一天，记得记录今日健康数据哦</p>
        </div>
      </div>
    </div>

    <div class="px-4 mt-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">常用功能</h2>
      <div class="grid grid-cols-2 gap-4">
        <div
          v-for="item in features"
          :key="item.name"
          @click="goTo(item.path)"
          class="bg-white rounded-2xl p-5 shadow-md hover:shadow-lg transition-all cursor-pointer active:scale-95"
        >
          <div class="text-4xl mb-3">{{ item.icon }}</div>
          <h3 class="font-semibold text-gray-800">{{ item.name }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ item.desc }}</p>
        </div>
      </div>
    </div>

    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-6 py-3 flex justify-around">
      <div class="text-orange-500 text-center">
        <div class="text-2xl">🏠</div>
        <p class="text-xs mt-1">首页</p>
      </div>
      <div @click="goTo('/elder/chat')" class="text-gray-400 text-center cursor-pointer">
        <div class="text-2xl">💬</div>
        <p class="text-xs mt-1">聊天</p>
      </div>
      <div @click="goTo('/elder/emergency')" class="text-gray-400 text-center cursor-pointer">
        <div class="text-2xl">🆘</div>
        <p class="text-xs mt-1">求助</p>
      </div>
      <div @click="goTo('/elder/profile')" class="text-gray-400 text-center cursor-pointer">
        <div class="text-2xl">👤</div>
        <p class="text-xs mt-1">我的</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { getHealthSummary } from '../../api/health'

const router = useRouter()
const userStore = useUserStore()

const healthData = ref({
  bloodPressure: '',
  heartRate: ''
})

const healthStatus = ref({
  bloodPressure: false,
  heartRate: false
})

const lastUpdateTime = ref('加载中...')
const showNewDayAlert = ref(false)

let syncTimer: ReturnType<typeof setInterval> | null = null

const greeting = computed(() => {
  const hour = new Date().getHours()
  if (hour < 6) return '夜深了，注意休息'
  if (hour < 12) return '早上好'
  if (hour < 14) return '中午好'
  if (hour < 18) return '下午好'
  return '晚上好'
})

const features = [
  { name: '智能聊天', icon: '💬', desc: '陪您说说话', path: '/elder/chat' },
  { name: '用药提醒', icon: '💊', desc: '按时吃药', path: '/elder/medication' },
  { name: '紧急求助', icon: '🆘', desc: '一键呼救', path: '/elder/emergency' },
  { name: '视频通话', icon: '📹', desc: '见见家人', path: '/elder/video-call' },
  { name: '健康记录', icon: '💚', desc: '记录健康', path: '/elder/health' },
]

function goTo(path: string) {
  router.push(path)
}

function checkNewDay() {
  const today = new Date().toISOString().split('T')[0]
  const lastDate = localStorage.getItem('lastHealthDate')
  
  if (lastDate && lastDate !== today) {
    showNewDayAlert.value = true
  }
  
  localStorage.setItem('lastHealthDate', today)
}

async function loadHealthData() {
  if (!userStore.userInfo?.id) return
  
  try {
    const res: any = await getHealthSummary(userStore.userInfo.id)
    
    healthData.value = {
      bloodPressure: res.latest_blood_pressure || '',
      heartRate: res.latest_heart_rate || ''
    }
    
    healthStatus.value = {
      bloodPressure: res.blood_pressure_status === 'abnormal',
      heartRate: res.heart_rate_status === 'abnormal'
    }
    
    const now = new Date()
    lastUpdateTime.value = `${now.getHours()}:${String(now.getMinutes()).padStart(2, '0')} 更新`
  } catch (error) {
    console.error('加载健康数据失败', error)
  }
}

onMounted(() => {
  loadHealthData()
  checkNewDay()
  
  syncTimer = setInterval(() => {
    loadHealthData()
    checkNewDay()
  }, 30000)
})

onUnmounted(() => {
  if (syncTimer) {
    clearInterval(syncTimer)
  }
})
</script>