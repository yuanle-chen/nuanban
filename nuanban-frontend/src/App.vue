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
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from './stores/user'
import { getCurrentUser } from './api/auth'
import { getTodayMedication, takeMedication } from './api/medication'

const userStore = useUserStore()
const showMedAlert = ref(false)
const medAlertItem = ref<any>(null)

async function checkMedication() {
  // 只有老人端且已登录才检查
  if (!userStore.userInfo?.id || userStore.userInfo.role !== 'elder') return

  try {
    const res: any = await getTodayMedication(userStore.userInfo.id)
    const now = new Date()
    const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`

    for (const item of res) {
      if (item.status !== 'taken' && item.scheduled_time === timeStr) {
        medAlertItem.value = item
        showMedAlert.value = true
        break
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

let timer: ReturnType<typeof setInterval> | null = null

onMounted(async () => {
  // 获取用户信息
  if (userStore.token && !userStore.userInfo) {
    try {
      const res: any = await getCurrentUser()
      userStore.setUserInfo(res)
    } catch (error) {
      console.log('获取用户信息失败')
    }
  }

  // 启动全局定时器，每30秒检查一次用药提醒
  timer = setInterval(() => {
    checkMedication()
  }, 30000)
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
</style>
