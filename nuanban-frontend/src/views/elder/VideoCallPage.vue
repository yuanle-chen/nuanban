<template>
  <div class="min-h-screen bg-black flex flex-col text-white">
    <div class="flex-1 relative bg-gradient-to-b from-gray-800 to-gray-900">
      <div class="absolute top-4 left-4 flex items-center gap-3 z-10">
        <button @click="goBack" class="w-10 h-10 bg-black/40 rounded-full flex items-center justify-center text-white">
          ←
        </button>
      </div>

      <div v-if="!callId && children.length === 0" class="absolute inset-0 flex items-center justify-center">
        <div class="text-center">
          <div class="text-8xl mb-4">📞</div>
          <p class="text-xl text-white/80">正在加载子女列表...</p>
        </div>
      </div>

      <div v-else-if="!callId && children.length > 0" class="absolute inset-0 p-6 overflow-y-auto">
        <h2 class="text-xl font-bold mb-6 text-center">选择通话对象</h2>
        <div class="space-y-4">
          <div
            v-for="child in children"
            :key="child.id"
            @click="handleStartCall(child)"
            class="bg-gray-700/50 rounded-2xl p-6 flex items-center justify-between active:scale-95 transition-transform cursor-pointer"
          >
            <div class="flex items-center gap-4">
              <div class="w-16 h-16 bg-blue-500 rounded-full flex items-center justify-center text-3xl">👩</div>
              <div>
                <h3 class="text-xl font-semibold">{{ child.username }}</h3>
                <p class="text-sm text-white/60">{{ child.relation_type || '子女' }}</p>
              </div>
            </div>
            <div class="w-12 h-12 bg-green-500 rounded-full flex items-center justify-center">📹</div>
          </div>
        </div>
      </div>

      <div v-else class="absolute inset-0 flex items-center justify-center">
        <div class="text-center">
          <div class="text-8xl mb-4">{{ isIncoming ? '👩' : '👩' }}</div>
          <p class="text-2xl text-white/80">{{ childName }}</p>
          <p class="text-lg text-white/60 mt-2">
            <span v-if="callStatus === 'calling'" class="animate-pulse">
              {{ isIncoming ? '来电中...' : '呼叫中...' }}
            </span>
            <span v-else-if="callStatus === 'connected'">通话中 {{ formatDuration(duration) }}</span>
            <span v-else-if="callStatus === 'ended'">通话已结束</span>
            <span v-else-if="callStatus === 'missed'">未接通</span>
          </p>
        </div>
      </div>

      <div v-if="callId" class="absolute top-4 right-4 w-28 h-40 bg-gray-700 rounded-xl overflow-hidden border-2 border-white/20 shadow-lg">
        <div class="w-full h-full flex items-center justify-center text-3xl bg-gray-600">
          👴
        </div>
      </div>
    </div>

    <div class="bg-gray-900/90 px-6 py-12">
      <div v-if="isIncoming && callStatus === 'calling'" class="flex justify-around items-center">
        <button
          @click="handleReject"
          class="w-20 h-20 rounded-full bg-red-500 flex items-center justify-center text-3xl shadow-lg active:scale-95 transition-transform"
        >
          📞
        </button>

        <button
          @click="handleAccept"
          class="w-20 h-20 rounded-full bg-green-500 flex items-center justify-center text-3xl shadow-lg active:scale-95 transition-transform animate-bounce"
        >
          📞
        </button>
      </div>

      <div v-else-if="callId" class="flex justify-around items-center">
        <button
          @click="toggleMute"
          class="w-16 h-16 rounded-full flex items-center justify-center text-2xl transition-all"
          :class="isMuted ? 'bg-red-500' : 'bg-gray-700'"
        >
          {{ isMuted ? '🔇' : '🎤' }}
        </button>

        <button
          v-if="callStatus !== 'ended' && callStatus !== 'missed'"
          @click="handleEndCall"
          class="w-20 h-20 rounded-full bg-red-500 flex items-center justify-center text-3xl shadow-lg active:scale-95 transition-transform"
        >
          📞
        </button>

        <div v-else class="w-20 h-20"></div>

        <button
          @click="toggleCamera"
          class="w-16 h-16 rounded-full bg-gray-700 flex items-center justify-center text-2xl"
        >
          📷
        </button>
      </div>

      <div v-if="callId" class="flex justify-around mt-3 text-lg text-white/60">
        <template v-if="isIncoming && callStatus === 'calling'">
          <span class="text-red-400">挂断</span>
          <span class="text-green-400">接听</span>
        </template>
        <template v-else>
          <span>{{ isMuted ? '已静音' : '麦克风' }}</span>
          <span v-if="callStatus !== 'ended' && callStatus !== 'missed'">挂断</span>
          <span v-else> </span>
          <span>摄像头</span>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { acceptCall, endCall, getPendingCalls, startVideoCall, getCallHistory } from '../../api/videoCall'
import { useFamilyStore } from '../../stores/family'

const router = useRouter()
const route = useRoute()
const familyStore = useFamilyStore()

const callId = ref<number | null>(null)
const callStatus = ref<'calling' | 'connected' | 'ended' | 'missed'>('calling')
const duration = ref(0)
const isMuted = ref(false)
const isCameraOn = ref(true)
const isIncoming = ref(false)
const childName = ref('子女')
const children = ref<any[]>([])

let durationTimer: ReturnType<typeof setInterval> | null = null
let pollTimer: ReturnType<typeof setInterval> | null = null

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

function startDurationTimer() {
  durationTimer = setInterval(() => {
    duration.value++
  }, 1000)
}

async function handleStartCall(child: any) {
  try {
    const res: any = await startVideoCall(child.id)
    callId.value = res.id
    childName.value = child.username
    isIncoming.value = false
    callStatus.value = 'calling'
    pollCallStatus()
  } catch (err: any) {
    alert(err.response?.data?.detail || '发起通话失败')
  }
}

async function handleAccept() {
  if (!callId.value) return
  try {
    await acceptCall(callId.value)
    callStatus.value = 'connected'
    startDurationTimer()
  } catch (err) {
    console.error('接听失败', err)
    alert('接听失败')
  }
}

async function handleReject() {
  if (callId.value) {
    try {
      await endCall(callId.value)
    } catch (err) {
      console.error('挂断失败', err)
    }
  }
  callStatus.value = 'missed'
  router.back()
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
  if (pollTimer) clearInterval(pollTimer)
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

async function pollCallStatus() {
  if (!callId.value) return

  const checkStatus = async () => {
    try {
      const calls: any = await getPendingCalls()
      if (callStatus.value === 'calling') {
        for (const call of calls) {
          if (call.id === callId.value && call.status === 'connected') {
            callStatus.value = 'connected'
            startDurationTimer()
            if (pollTimer) clearInterval(pollTimer)
            return
          }
        }
      }
      if (callStatus.value === 'calling' || callStatus.value === 'connected') {
        const callHistory: any = await getCallHistory()
        for (const call of callHistory) {
          if (call.id === callId.value && (call.status === 'ended' || call.status === 'missed')) {
            callStatus.value = call.status
            if (durationTimer) clearInterval(durationTimer)
            if (pollTimer) clearInterval(pollTimer)
            router.back()
            return
          }
        }
      }
    } catch (err) {
      console.error('检查通话状态失败', err)
    }
  }

  pollTimer = setInterval(checkStatus, 2000)
}

async function checkIncoming() {
  try {
    const calls: any = await getPendingCalls()
    if (calls && calls.length > 0 && !callId.value) {
      const call = calls[0]
      callId.value = call.id
      isIncoming.value = true
      childName.value = call.caller_name || '子女'
      callStatus.value = 'calling'
      pollCallStatus()
    }
  } catch (err) {
    console.error('检查来电失败', err)
  }
}

onMounted(async () => {
  isIncoming.value = route.query.incoming === 'true'
  const incomingCallId = route.query.call_id ? Number(route.query.call_id) : null
  childName.value = (route.query.name as string) || '子女'

  if (isIncoming.value && incomingCallId) {
    callId.value = incomingCallId
    callStatus.value = 'calling'
    pollCallStatus()
  } else {
    try {
      const res: any = await familyStore.fetchChildren()
      children.value = res || []
      if (children.value.length === 0) {
        checkIncoming()
        pollTimer = setInterval(checkIncoming, 3000)
      }
    } catch (err) {
      console.error('获取子女列表失败', err)
    }
  }
})

onUnmounted(() => {
  if (durationTimer) clearInterval(durationTimer)
  if (pollTimer) clearInterval(pollTimer)
})
</script>

<style scoped>
.animate-bounce {
  animation: bounce 1s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}

.animate-pulse {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}
</style>
