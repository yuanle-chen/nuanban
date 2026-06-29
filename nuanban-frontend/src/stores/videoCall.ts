import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getPendingCalls } from '../api/videoCall'
import { speak, stopSpeaking } from '../utils/speech'

export const useVideoCallStore = defineStore('videoCall', () => {
  const incomingCall = ref<any>(null)
  const isPolling = ref(false)
  let pollTimer: ReturnType<typeof setInterval> | null = null
  let lastCallId: number | null = null

  function startPolling(role: 'elder' | 'child') {
    if (isPolling.value) return
    isPolling.value = true

    const checkCalls = async () => {
      try {
        const calls: any = await getPendingCalls()
        if (calls && calls.length > 0) {
          const call = calls[0]
          if (!incomingCall.value || incomingCall.value.id !== call.id) {
            incomingCall.value = call
            if (call.id !== lastCallId) {
              lastCallId = call.id
              const name = role === 'elder'
                ? (call.caller_name || '家人')
                : (call.caller_name || '老人')
              speak(`${name}发来视频通话，请接听`)
            }
          }
        } else {
          if (incomingCall.value) {
            stopSpeaking()
          }
          incomingCall.value = null
        }
      } catch (err) {
        console.error('检查来电失败', err)
      }
    }

    checkCalls()
    pollTimer = setInterval(checkCalls, 5000)
  }

  function stopPolling() {
    if (pollTimer) {
      clearInterval(pollTimer)
      pollTimer = null
    }
    isPolling.value = false
    incomingCall.value = null
    lastCallId = null
    stopSpeaking()
  }

  function clearIncoming() {
    incomingCall.value = null
    stopSpeaking()
  }

  return {
    incomingCall,
    isPolling,
    startPolling,
    stopPolling,
    clearIncoming
  }
})
