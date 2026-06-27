<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-purple-500 to-pink-400 text-white p-6 pb-16 rounded-b-3xl">
      <div class="flex items-center gap-3 mb-4">
        <button @click="$router.back()" class="text-white text-lg">← 返回</button>
        <h1 class="text-xl font-bold">用药提醒</h1>
      </div>
      <p class="text-white/80 text-sm">今日共 {{ todayList.length }} 次用药</p>
    </div>

    <!-- 今日用药列表 -->
    <div class="px-4 -mt-8">
      <div class="bg-white rounded-2xl p-6 shadow-md">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">今日用药</h2>

        <div v-if="todayList.length === 0" class="text-center text-gray-400 py-8">
          <p class="text-4xl mb-2">💊</p>
          <p>暂无用药计划</p>
        </div>

        <div v-else class="space-y-3">
          <div
            v-for="item in todayList"
            :key="`${item.plan_id}-${item.scheduled_time}`"
            :class="[
              'p-4 rounded-2xl border-2 transition-all',
              item.status === 'taken'
                ? 'bg-green-50 border-green-200'
                : isPast(item.scheduled_time)
                ? 'bg-red-50 border-red-200'
                : 'bg-gray-50 border-gray-100'
            ]"
          >
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div
                  :class="[
                    'w-14 h-14 rounded-full flex items-center justify-center text-2xl',
                    item.status === 'taken'
                      ? 'bg-green-200'
                      : isPast(item.scheduled_time)
                      ? 'bg-red-200'
                      : 'bg-purple-100'
                  ]"
                >
                  {{ item.status === 'taken' ? '✅' : '💊' }}
                </div>
                <div>
                  <p class="text-lg font-bold text-gray-800">{{ item.medication_name }}</p>
                  <p class="text-sm text-gray-500">{{ item.dosage }} · {{ item.scheduled_time }}</p>
                </div>
              </div>

              <button
                v-if="item.status !== 'taken'"
                @click="handleTake(item)"
                class="px-6 py-2 bg-gradient-to-r from-purple-500 to-pink-400 text-white font-semibold rounded-full text-sm hover:opacity-90"
              >
                已服用
              </button>
              <span v-else class="text-green-600 font-semibold text-sm">
                已服用
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 温馨提示 -->
    <div class="px-4 mt-6">
      <div class="bg-purple-50 rounded-2xl p-4">
        <p class="text-sm text-purple-700">
          💡 温馨提示：请按时服药，如有不适请及时联系家人或就医。
        </p>
      </div>
    </div>

    <!-- 自动弹窗提醒 -->
    <div
      v-if="showAlert && alertItem"
      class="fixed top-4 left-4 right-4 z-50 animate-slide-down"
    >
      <div class="bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-2xl p-4 shadow-lg flex items-center justify-between">
        <div class="flex items-center gap-3">
          <span class="text-3xl">💊</span>
          <div>
            <p class="font-bold text-lg">该吃药啦！</p>
            <p class="text-white/90">{{ alertItem.medication_name }} - {{ alertItem.dosage }}</p>
          </div>
        </div>
        <button
          @click="handleAlertTake"
          class="bg-white text-purple-600 font-bold px-4 py-2 rounded-full text-sm"
        >
          已服用
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { getTodayMedication, takeMedication } from '../../api/medication'

const userStore = useUserStore()
const todayList = ref<any[]>([])
const loading = ref(false)
const showAlert = ref(false)
const alertItem = ref<any>(null)

function isPast(time: string) {
  const now = new Date()
  const [h, m] = time.split(':').map(Number)
  const target = new Date()
  target.setHours(h, m, 0, 0)
  return now > target
}

async function loadToday() {
  if (!userStore.userInfo?.id) return
  try {
    const res: any = await getTodayMedication(userStore.userInfo.id)
    todayList.value = res
  } catch (error) {
    console.error('加载用药列表失败', error)
  }
}

async function handleTake(item: any) {
  if (!userStore.userInfo?.id) return
  loading.value = true
  try {
    await takeMedication(item.plan_id, item.scheduled_time, userStore.userInfo.id)
    alert('已记录服药！')
    await loadToday()
  } catch (err: any) {
    alert(err.response?.data?.detail || '操作失败')
  } finally {
    loading.value = false
  }
}

// 自动弹窗提醒
function checkTime() {
  const now = new Date()
  const timeStr = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`

  for (const item of todayList.value) {
    if (item.status !== 'taken' && item.scheduled_time === timeStr && !showAlert.value) {
      alertItem.value = item
      showAlert.value = true
      break
    }
  }
}

async function handleAlertTake() {
  if (!userStore.userInfo?.id || !alertItem.value) return
  try {
    await takeMedication(alertItem.value.plan_id, alertItem.value.scheduled_time, userStore.userInfo.id)
    showAlert.value = false
    alertItem.value = null
    await loadToday()
  } catch (err: any) {
    alert(err.response?.data?.detail || '操作失败')
  }
}

let timer: ReturnType<typeof setInterval> | null = null

onMounted(() => {
  loadToday()
  timer = setInterval(() => {
    checkTime()
  }, 5000) // 每5秒检查一次
})

onUnmounted(() => {
  if (timer) clearInterval(timer)
})
</script>

<style>
@keyframes slide-down {
  from { transform: translateY(-100%); opacity: 0; }
  to { transform: translateY(0); opacity: 1; }
}
.animate-slide-down {
  animation: slide-down 0.3s ease-out;
}
</style>
