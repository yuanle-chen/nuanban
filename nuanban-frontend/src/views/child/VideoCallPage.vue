<template>
  <div class="min-h-screen bg-black flex flex-col text-white">
    <!-- 视频区域 -->
    <div class="flex-1 relative bg-gradient-to-b from-gray-800 to-gray-900">
      <!-- 远端视频（老人） -->
      <div class="absolute inset-0 flex items-center justify-center">
        <div class="text-center">
          <div class="text-8xl mb-4">👴</div>
          <p class="text-xl text-white/80">{{ elderName }}</p>
          <p class="text-sm text-white/60 mt-2">
            <span v-if="callStatus === 'calling'" class="animate-pulse">呼叫中...</span>
            <span v-else-if="callStatus === 'connected'">通话中 {{ formatDuration(duration) }}</span>
            <span v-else-if="callStatus === 'ended'">通话已结束</span>
            <span v-else-if="callStatus === 'missed'">未接通</span>
          </p>
        </div>
      </div>

      <!-- 本地视频小窗口（自己） -->
      <div class="absolute top-4 right-4 w-28 h-40 bg-gray-700 rounded-xl overflow-hidden border-2 border-white/20 shadow-lg">
        <div class="w-full h-full flex items-center justify-center text-3xl bg-gray-600">
          👩
        </div>
      </div>

      <!-- 顶部信息 -->
      <div class="absolute top-4 left-4 flex items-center gap-3">
        <button @click="goBack" class="w-10 h-10 bg-black/40 rounded-full flex items-center justify-center text-white">
          ←
        </button>
      </div>
    </div>

    <!-- 底部控制栏 -->
    <div class="bg-gray-900/90 px-6 py-8">
      <div class="flex justify-around items-center">
        <!-- 静音按钮 -->
        <button
          @click="toggleMute"
          class="w-16 h-16 rounded-full flex items-center justify-center text-2xl transition-all"
          :class="isMuted ? 'bg-red-500' : 'bg-gray-700'"
        >
          {{ isMuted ? '🔇' : '🎤' }}
        </button>

        <!-- 挂断按钮 -->
        <button
          v-if="callStatus !== 'ended' && callStatus !== 'missed'"
          @click="handleEndCall"
          class="w-20 h-20 rounded-full bg-red-500 flex items-center justify-center text-3xl shadow-lg active:scale-95 transition-transform"
        >
          📞
        </button>

        <!-- 接听按钮（仅呼叫中显示，子女端发起的话不显示） -->
        <button
          v-if="isIncoming"
          @click="handleAccept"
          class="w-20 h-20 rounded-full bg-green-500 flex items-center justify-center text-3xl shadow-lg active:scale-95 transition-transform animate-pulse"
        >
          📞
        </button>

        <!-- 摄像头切换 -->
        <button
          @click="toggleCamera"
          class="w-16 h-16 rounded-full bg-gray-700 flex items-center justify-center text-2xl"
        >
          📷
        </button>
      </div>

      <div class="flex justify-around mt-3 text-xs text-white/60">
        <span>{{ isMuted ? '已静音' : '麦克风' }}</span>
        <span v-if="callStatus !== 'ended' && callStatus !== 'missed'">挂断</span>
        <span v-else> </span>
        <span>摄像头</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { startVideoCall, acceptCall, endCall, getCallHistory } from '../../api/videoCall'
import { useFamilyStore } from '../../stores/family'

const router = useRouter()
const route = useRoute()
const familyStore = useFamilyStore()

const callId = ref<number | null>(null)
const roomId = ref('')
const callStatus = ref<'calling' | 'connected' | 'ended' | 'missed'>('calling')
const duration = ref(0)
const isMuted = ref(false)
const isCameraOn = ref(true)
const isIncoming = ref(false)

let durationTimer: ReturnType<typeof setInterval> | null = null
let checkTimer: ReturnType<typeof setInterval> | null = null

const elderName = computed(() => {
  const elderId = route.query.elder_id ? Number(route.query.elder_id) : null
  if (elderId && familyStore.elders.length > 0) {
    const elder = familyStore.elders.find(e => e.id === elderId)
    return elder?.profile?.real_name || elder?.username || '老人'
  }
  return route.query.name as string || '老人'
})

function formatDuration(seconds: number) {
  const min = Math.floor(seconds / 60)
  const sec = seconds % 60
  return `${min.toString().padStart(2, '0')}:${sec.toString().padStart(2, '0')}`
}

function toggleMute() {
  isMuted.value = !isMuted.value
}

function toggleCamera() {
  isCameraOn.value = !isCameraOn.value
}

async function handleStartCall() {
  const elderId = route.query.elder_id ? Number(route.query.elder_id) : null
  if (!elderId) {
    alert('缺少老人ID')
    router.back()
    return
  }

  try {
    const res: any = await startVideoCall(elderId)
    callId.value = res.id
    roomId.value = res.room_id
    callStatus.value = 'calling'
    pollCallStatus()
  } catch (err: any) {
    alert(err.response?.data?.detail || '发起通话失败')
    router.back()
  }
}

function startDurationTimer() {
  durationTimer = setInterval(() => {
    duration.value++
  }, 1000)
}

async function pollCallStatus() {
  if (!callId.value) return

  const checkStatus = async () => {
    try {
      const history: any = await getCallHistory()
      for (const call of history) {
        if (call.id === callId.value) {
          if (call.status === 'connected' && callStatus.value === 'calling') {
            callStatus.value = 'connected'
            startDurationTimer()
          } else if (call.status === 'ended' || call.status === 'missed') {
            callStatus.value = call.status
            if (durationTimer) clearInterval(durationTimer)
            if (checkTimer) clearInterval(checkTimer)
            router.back()
          }
          return
        }
      }
    } catch (err) {
      console.error('检查通话状态失败', err)
    }
  }

  checkTimer = setInterval(checkStatus, 2000)
}

async function handleAccept() {
  if (!callId.value) return
  try {
    await acceptCall(callId.value)
    callStatus.value = 'connected'
    startDurationTimer()
  } catch (err) {
    console.error('接听失败', err)
  }
}

async function handleEndCall() {
  if (!callId.value) {
    router.back()
    return
  }

  try {
    await endCall(callId.value)
  } catch (err) {
    console.error('结束通话失败', err)
  }

  callStatus.value = 'ended'
  if (durationTimer) clearInterval(durationTimer)
  if (checkTimer) clearInterval(checkTimer)
  router.back()
}

function goBack() {
  if (callStatus.value === 'connected' || callStatus.value === 'calling') {
    if (confirm('确定要挂断吗？')) {
      handleEndCall()
    }
  } else {
    router.back()
  }
}

onMounted(() => {
  isIncoming.value = route.query.incoming === 'true'
  const incomingCallId = route.query.call_id ? Number(route.query.call_id) : null

  if (isIncoming.value && incomingCallId) {
    callId.value = incomingCallId
    callStatus.value = 'calling'
  } else {
    handleStartCall()
  }
})

onUnmounted(() => {
  if (durationTimer) clearInterval(durationTimer)
  if (checkTimer) clearInterval(checkTimer)
})
</script>

<style scoped>
.animate-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.8; transform: scale(1.05); }
}
</style>
