<template>
  <div
    v-if="videoCallStore.incomingCall"
    class="fixed inset-0 z-50 flex items-center justify-center bg-black/70"
  >
    <div class="bg-gray-900 rounded-3xl p-8 w-80 text-center">
      <div class="text-6xl mb-4 animate-bounce">
        {{ isElder ? '👩' : '👴' }}
      </div>
      <h2 class="text-xl font-bold text-white mb-2">
        {{ videoCallStore.incomingCall.caller_name || '家人' }}
      </h2>
      <p class="text-gray-400 mb-8">发来视频通话</p>

      <div class="flex justify-around">
        <button
          @click="handleReject"
          class="w-16 h-16 rounded-full bg-red-500 flex items-center justify-center text-2xl shadow-lg active:scale-95 transition-transform"
        >
          📞
        </button>
        <button
          @click="handleAccept"
          class="w-16 h-16 rounded-full bg-green-500 flex items-center justify-center text-2xl shadow-lg active:scale-95 transition-transform animate-bounce"
        >
          📞
        </button>
      </div>
      <div class="flex justify-around mt-3">
        <span class="text-red-400 text-sm">挂断</span>
        <span class="text-green-400 text-sm">接听</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useVideoCallStore } from '../stores/videoCall'
import { useUserStore } from '../stores/user'
import { acceptCall, endCall } from '../api/videoCall'
import { stopSpeaking } from '../utils/speech'

const router = useRouter()
const videoCallStore = useVideoCallStore()
const userStore = useUserStore()

const isElder = computed(() => userStore.userInfo?.role === 'elder')

function handleAccept() {
  stopSpeaking()
  const call = videoCallStore.incomingCall
  if (!call) return

  acceptCall(call.id).catch(() => {})

  const name = call.caller_name || '家人'
  const path = isElder.value ? '/elder/video-call' : '/child/video-call'

  videoCallStore.clearIncoming()
  router.push({
    path,
    query: {
      incoming: 'true',
      call_id: call.id,
      name
    }
  })
}

function handleReject() {
  stopSpeaking()
  const call = videoCallStore.incomingCall
  if (call) {
    endCall(call.id).catch(() => {})
  }
  videoCallStore.clearIncoming()
}
</script>

<style scoped>
.animate-bounce {
  animation: bounce 1s ease-in-out infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-8px); }
}
</style>
