<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-red-500 to-orange-500 text-white p-6 pt-10 pb-16 rounded-b-3xl">
      <div class="flex items-center gap-3 mb-4">
        <button @click="$router.back()" class="text-white text-lg">← 返回</button>
        <h1 class="text-xl font-bold">紧急求助</h1>
      </div>
      <p class="text-white/80 text-sm">有 {{ pendingCount }} 条待处理求助</p>
    </div>

    <!-- 待处理求助 -->
    <div class="px-4 -mt-8">
      <div v-if="pending.length > 0" class="bg-white rounded-2xl p-5 shadow-md border-2 border-red-200">
        <h2 class="text-lg font-semibold text-red-600 mb-4 flex items-center gap-2">
          <span class="w-3 h-3 bg-red-500 rounded-full animate-pulse"></span>
          紧急求助
        </h2>
        <div class="space-y-4">
          <div
            v-for="item in pending"
            :key="item.id"
            class="bg-red-50 rounded-xl p-4"
          >
            <div class="flex items-start justify-between mb-3">
              <div class="flex items-center gap-3">
                <div class="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center text-2xl">
                  {{ getAlertIcon(item.alert_type) }}
                </div>
                <div>
                  <p class="font-bold text-gray-800">{{ getAlertName(item.alert_type) }}</p>
                  <p class="text-sm text-gray-500">{{ item.elder_name }} · {{ formatTime(item.created_at) }}</p>
                </div>
              </div>
              <span class="px-3 py-1 bg-red-500 text-white text-xs font-medium rounded-full">
                紧急
              </span>
            </div>
            <div class="flex gap-2">
              <button
                @click="callElder(item)"
                class="flex-1 py-2 bg-green-500 text-white font-semibold rounded-xl text-sm hover:bg-green-600 flex items-center justify-center gap-1"
              >
                📞 拨打电话
              </button>
              <button
                @click="handleEmergency(item.id, 'contacting')"
                class="flex-1 py-2 bg-blue-500 text-white font-semibold rounded-xl text-sm hover:bg-blue-600"
              >
                标记联系中
              </button>
              <button
                @click="handleEmergency(item.id, 'resolved')"
                class="flex-1 py-2 bg-green-500 text-white font-semibold rounded-xl text-sm hover:bg-green-600"
              >
                已解决
              </button>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="bg-white rounded-2xl p-8 shadow-md text-center">
        <p class="text-5xl mb-3">✅</p>
        <p class="text-gray-600 font-medium">暂无紧急求助</p>
        <p class="text-sm text-gray-400 mt-1">所有求助都已处理</p>
      </div>
    </div>

    <!-- 历史记录 -->
    <div class="px-4 mt-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">处理记录</h2>
      <div class="bg-white rounded-2xl shadow-md divide-y divide-gray-100">
        <div
          v-for="item in history"
          :key="item.id"
          class="p-4 flex items-center gap-3"
        >
          <div :class="[
            'w-10 h-10 rounded-full flex items-center justify-center text-xl',
            getAlertBgClass(item.alert_type)
          ]">
            {{ getAlertIcon(item.alert_type) }}
          </div>
          <div class="flex-1">
            <p class="font-medium text-gray-800">{{ item.elder_name }} - {{ getAlertName(item.alert_type) }}</p>
            <p class="text-xs text-gray-400">{{ formatTime(item.created_at) }}</p>
          </div>
          <span :class="[
            'px-3 py-1 rounded-full text-xs font-medium',
            item.handled_status === 'pending' ? 'bg-yellow-100 text-yellow-600' :
            item.handled_status === 'contacting' ? 'bg-blue-100 text-blue-600' :
            item.handled_status === 'resolved' ? 'bg-green-100 text-green-600' :
            'bg-gray-100 text-gray-600'
          ]">
            {{ getStatusName(item.handled_status) }}
          </span>
        </div>
        <div v-if="history.length === 0" class="p-8 text-center text-gray-400">
          暂无处理记录
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useFamilyStore } from '../../stores/family'
import { getPendingEmergencies, handleEmergency } from '../../api/emergency'
import { getEmergencyHistory } from '../../api/emergency'

const familyStore = useFamilyStore()
const pending = ref<any[]>([])
const history = ref<any[]>([])

const pendingCount = computed(() => pending.value.length)

async function loadPending() {
  try {
    const res: any = await getPendingEmergencies()
    pending.value = res.map((item: any) => {
      const elder = familyStore.elders.find((e: any) => e.id === item.elder_user_id)
      return {
        ...item,
        elder_name: elder?.profile?.real_name || elder?.username || '未知老人'
      }
    })
  } catch (error) {
    console.error('加载待处理求助失败', error)
  }
}

async function loadHistory() {
  if (!familyStore.currentElder?.id) return
  try {
    const res: any = await getEmergencyHistory(familyStore.currentElder.id, 20)
    history.value = res.map((item: any) => {
      const elder = familyStore.elders.find((e: any) => e.id === item.elder_user_id)
      return {
        ...item,
        elder_name: elder?.profile?.real_name || elder?.username || '未知老人'
      }
    })
  } catch (error) {
    console.error('加载历史记录失败', error)
  }
}

async function handleEmergencyAction(recordId: number, status: string) {
  try {
    await handleEmergency(recordId, status)
    alert(status === 'contacting' ? '正在联系...' : '已标记为解决')
    await loadPending()
    await loadHistory()
  } catch (err: any) {
    alert(err.response?.data?.detail || '操作失败')
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

function callElder(item: any) {
  const elder = familyStore.elders.find((e: any) => e.id === item.elder_user_id)
  const phone = elder?.phone
  if (!phone) {
    alert('该老人未绑定手机号，请通过其他方式联系')
    return
  }
  window.location.href = `tel:${phone}`
}

function formatTime(time: string) {
  const d = new Date(time)
  return `${d.getMonth() + 1}月${d.getDate()}日 ${d.getHours()}:${String(d.getMinutes()).padStart(2, '0')}`
}

onMounted(async () => {
  if (!familyStore.currentElder) {
    await familyStore.fetchElders()
  }
  loadPending()
  loadHistory()
})
</script>
