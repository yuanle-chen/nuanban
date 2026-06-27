<template>
  <router-view />

  <!-- 全局用药提醒弹窗（仅老人端显示） -->
  <div
    v-if="showMedAlert && medAlertItem && userStore.userInfo?.role === 'elder'"
    class="fixed top-4 left-4 right-4 z-[9999] animate-slide-down"
  >
    <div class="bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-2xl p-4 shadow-2xl flex items-center justify-between">
      <div class="flex items-center gap-3">
        <span class="text-3xl">💊</span>
        <div>
          <p class="font-bold text-lg">该吃药啦！</p>
          <p class="text-white/90">{{ medAlertItem.medication_name }} - {{ medAlertItem.dosage }}</p>
        </div>
      </div>
      <div class="flex gap-2">
        <button
          @click="handleMedTake"
          class="bg-white text-purple-600 font-bold px-4 py-2 rounded-full text-sm"
        >
          已服用
        </button>
        <button
          @click="dismissAlert"
          class="bg-white/20 text-white font-bold px-3 py-2 rounded-full text-sm"
        >
          稍后
        </button>
      </div>
    </div>
  </div>

  <!-- 全局紧急求助弹窗（仅子女端显示） -->
  <div
    v-if="showEmergencyAlert && emergencyAlertItem && userStore.userInfo?.role === 'child'"
    class="fixed top-4 left-4 right-4 z-[9999] animate-shake"
  >
    <div class="bg-gradient-to-r from-red-500 to-orange-500 text-white rounded-2xl p-4 shadow-2xl">
      <div class="flex items-center justify-between mb-3">
        <div class="flex items-center gap-3">
          <span class="text-3xl animate-pulse">🆘</span>
          <div>
            <p class="font-bold text-lg">紧急求助！</p>
            <p class="text-white/90">{{ emergencyAlertItem.elder_name }} - {{ getEmergencyName(emergencyAlertItem.alert_type) }}</p>
          </div>
        </div>
        <button
          @click="dismissEmergencyAlert"
          class="bg-white/20 text-white px-3 py-1 rounded-full text-sm"
        >
          稍后查看
        </button>
      </div>
      <div class="flex gap-2">
        <button
          @click="callElderFromAlert"
          class="flex-1 py-2 bg-green-500 text-white font-bold rounded-xl text-sm flex items-center justify-center gap-1"
        >
          📞 拨打电话
        </button>
        <button
          @click="goToEmergency"
          class="flex-1 py-2 bg-white text-red-600 font-bold rounded-xl text-sm"
        >
          立即处理
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from './stores/user'
import { getCurrentUser } from './api/auth'
import { getTodayMedication, takeMedication } from './api/medication'
import { getPendingEmergencies } from './api/emergency'
import { useFamilyStore } from './stores/family'

const router = useRouter()
const userStore = useUserStore()
const familyStore = useFamilyStore()

const showMedAlert = ref(false)
const medAlertItem = ref<any>(null)

const showEmergencyAlert = ref(false)
const emergencyAlertItem = ref<any>(null)
const seenEmergencyIds = ref<number[]>([])

async function checkMedication() {
  if (!userStore.userInfo?.id || userStore.userInfo.role !== 'elder') return

  try {
    const res: any = await getTodayMedication(userStore.userInfo.id)
    const now = new Date()
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`

    for (const item of res) {
      if (item.status !== 'taken' && item.scheduled_time === timeStr && !showMedAlert.value) {
        medAlertItem.value = item
        showMedAlert.value = true
        break
      }
    }
  } catch (error) {
    // 忽略错误
  }
}

async function checkEmergency() {
  if (!userStore.userInfo?.id || userStore.userInfo.role !== 'child') return

  try {
    if (familyStore.elders.length === 0) {
      await familyStore.fetchElders()
    }

    const res: any = await getPendingEmergencies()
    if (res.length > 0) {
      const newItem = res.find((item: any) => !seenEmergencyIds.value.includes(item.id))
      if (newItem && !showEmergencyAlert.value) {
        const elder = familyStore.elders.find((e: any) => e.id === newItem.elder_user_id)
        emergencyAlertItem.value = {
          ...newItem,
          elder_name: elder?.profile?.real_name || elder?.username || '未知老人'
        }
        showEmergencyAlert.value = true
        seenEmergencyIds.value.push(newItem.id)
      }
    }
  } catch (error) {
    // 忽略错误
  }
}

async function handleMedTake() {
  if (!userStore.userInfo?.id || !medAlertItem.value) return
  try {
    await takeMedication(medAlertItem.value.plan_id, medAlertItem.value.scheduled_time, userStore.userInfo.id)
    showMedAlert.value = false
    medAlertItem.value = null
  } catch (error) {
    console.error('操作失败', error)
  }
}

function dismissAlert() {
  showMedAlert.value = false
}

function dismissEmergencyAlert() {
  showEmergencyAlert.value = false
}

function goToEmergency() {
  showEmergencyAlert.value = false
  router.push('/child/alerts')
}

function callElderFromAlert() {
  if (!emergencyAlertItem.value) return
  const elder = familyStore.elders.find((e: any) => e.id === emergencyAlertItem.value.elder_user_id)
  const phone = elder?.phone
  if (!phone) {
    alert('该老人未绑定手机号，请通过其他方式联系')
    return
  }
  window.location.href = `tel:${phone}`
}

function getEmergencyName(type: string) {
  const names: Record<string, string> = {
    sos: '紧急求助', fall: '跌倒报警', abnormal: '异常报警', voice: '语音求助'
  }
  return names[type] || type
}

let timer: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  if (userStore.token && !userStore.userInfo) {
    try {
      const res: any = await getCurrentUser()
      userStore.setUserInfo(res)
    } catch (error) {
      console.log('获取用户信息失败')
    }
  }

  timer = setInterval(() => {
    checkMedication()
    checkEmergency()
  }, 30000)

  setTimeout(() => {
    checkEmergency()
  }, 2000)
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style>
@keyframes slide-down {
  from { transform: translateY(-120%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.animate-slide-down {
  animation: slide-down 0.4s ease-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-8px); }
  40%, 80% { transform: translateX(8px); }
}
.animate-shake {
  animation: shake 0.5s ease-in-out, slide-down 0.4s ease-out;
}
</style>
