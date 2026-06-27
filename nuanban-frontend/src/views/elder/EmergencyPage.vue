<template>
  <div class="min-h-screen bg-gradient-to-br from-red-50 to-orange-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-red-500 to-orange-500 text-white p-6 pt-10 pb-16 rounded-b-3xl">
      <div class="flex items-center gap-3 mb-4">
        <button @click="$router.back()" class="text-white text-lg">← 返回</button>
        <h1 class="text-xl font-bold">紧急求助</h1>
      </div>
      <p class="text-white/80 text-sm">遇到紧急情况，一键求助家人</p>
    </div>

    <!-- SOS 大按钮 -->
    <div class="px-4 -mt-8">
      <div class="bg-white rounded-2xl p-6 shadow-md text-center">
        <button
          @click="handleSOS"
          :disabled="sending || recentRecord"
          :class="[
            'w-48 h-48 rounded-full text-4xl font-bold shadow-lg transition-all',
            sending ? 'bg-gray-300 text-gray-500' : 'bg-gradient-to-br from-red-500 to-red-600 text-white hover:shadow-xl active:scale-95'
          ]"
        >
          <span v-if="sending">发送中...</span>
          <span v-else-if="recentRecord">已发送</span>
          <span v-else>🆘<br>SOS</span>
        </button>
        <p class="mt-6 text-gray-600 font-medium">
          {{ recentRecord ? '求助已发送，家人正在赶来！' : '点击按钮发送紧急求助' }}
        </p>
        <p class="text-sm text-gray-400 mt-2">点击后您的位置将发送给您的家人</p>
      </div>
    </div>

    <!-- 其他求助类型 -->
    <div class="px-4 mt-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">其他求助</h2>
      <div class="grid grid-cols-2 gap-4">
        <button
          v-for="item in alertTypes"
          :key="item.type"
          @click="handleAlert(item.type)"
          :disabled="sending"
          class="bg-white rounded-2xl p-5 shadow-md hover:shadow-lg transition-all text-center"
        >
          <div class="text-4xl mb-2">{{ item.icon }}</div>
          <p class="font-medium text-gray-800">{{ item.name }}</p>
        </button>
      </div>
    </div>

    <!-- 历史记录 -->
    <div class="px-4 mt-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">最近求助</h2>
      <div class="bg-white rounded-2xl shadow-md divide-y divide-gray-100">
        <div
          v-for="record in history"
          :key="record.id"
          class="p-4 flex items-center justify-between"
        >
          <div class="flex items-center gap-3">
            <div :class="[
              'w-10 h-10 rounded-full flex items-center justify-center text-xl',
              getAlertBgClass(record.alert_type)
            ]">
              {{ getAlertIcon(record.alert_type) }}
            </div>
            <div>
              <p class="font-medium text-gray-800">{{ getAlertName(record.alert_type) }}</p>
              <p class="text-xs text-gray-400">{{ formatTime(record.created_at) }}</p>
            </div>
          </div>
          <span :class="[
            'px-3 py-1 rounded-full text-xs font-medium',
            record.handled_status === 'pending' ? 'bg-yellow-100 text-yellow-600' :
            record.handled_status === 'resolved' ? 'bg-green-100 text-green-600' :
            'bg-gray-100 text-gray-600'
          ]">
            {{ getStatusName(record.handled_status) }}
          </span>
        </div>
        <div v-if="history.length === 0" class="p-8 text-center text-gray-400">
          暂无求助记录
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useUserStore } from '../../stores/user'
import { triggerSOS, getEmergencyHistory } from '../../api/emergency'

const userStore = useUserStore()
const sending = ref(false)
const recentRecord = ref(false)
const history = ref<any[]>([])

const alertTypes = [
  { type: 'fall', name: '跌倒报警', icon: '🚶' },
  { type: 'abnormal', name: '异常报警', icon: '⚠️' },
  { type: 'voice', name: '语音求助', icon: '🎤' },
]

async function handleSOS() {
  if (!userStore.userInfo?.id || sending.value || recentRecord.value) return

  sending.value = true
  try {
    await triggerSOS(userStore.userInfo.id, 'sos')
    recentRecord.value = true
    alert('紧急求助已发送！家人正在赶来！')
    await loadHistory()
    setTimeout(() => {
      recentRecord.value = false
    }, 60000) // 1分钟内不重复发送
  } catch (err: any) {
    alert(err.response?.data?.detail || '发送失败，请重试')
  } finally {
    sending.value = false
  }
}

async function handleAlert(type: string) {
  if (!userStore.userInfo?.id) return
  try {
    await triggerSOS(userStore.userInfo.id, type)
    alert('求助已发送！')
    await loadHistory()
  } catch (err: any) {
    alert(err.response?.data?.detail || '发送失败，请重试')
  }
}

async function loadHistory() {
  if (!userStore.userInfo?.id) return
  try {
    const res: any = await getEmergencyHistory(userStore.userInfo.id, 10)
    history.value = res
  } catch (error) {
    console.error('加载历史失败', error)
  }
}

function getAlertIcon(type: string) {
  const icons: Record<string, string> = {
    sos: '🆘', fall: '🚶', abnormal: '⚠️', voice: '🎤'
  }
  return icons[type] || '🆘'
}

function getAlertName(type: string) {
  const names: Record<string, string> = {
    sos: '紧急求助', fall: '跌倒报警', abnormal: '异常报警', voice: '语音求助'
  }
  return names[type] || type
}

function getAlertBgClass(type: string) {
  const classes: Record<string, string> = {
    sos: 'bg-red-100', fall: 'bg-orange-100', abnormal: 'bg-yellow-100', voice: 'bg-blue-100'
  }
  return classes[type] || 'bg-gray-100'
}

function getStatusName(status: string) {
  const names: Record<string, string> = {
    pending: '待处理', contacting: '联系中', resolved: '已解决', cancelled: '已取消'
  }
  return names[status] || status
}

function formatTime(time: string) {
  const d = new Date(time)
  return `${d.getMonth() + 1}月${d.getDate()}日 ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}

onMounted(() => {
  loadHistory()
})
</script>
