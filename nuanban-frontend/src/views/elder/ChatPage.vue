<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 flex flex-col">
    <div class="bg-gradient-to-r from-orange-400 to-amber-500 text-white p-4 pt-10 pb-4">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 bg-white/20 rounded-full flex items-center justify-center text-xl">
          🤖
        </div>
        <div>
          <h1 class="text-lg font-bold">小暖</h1>
          <p class="text-orange-100 text-xs">您的贴心陪伴助手</p>
        </div>
      </div>
    </div>

    <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 pb-4">
      <div
        v-for="msg in messages"
        :key="msg.id"
        class="mb-4 flex"
        :class="msg.role === 'user' ? 'justify-end' : 'justify-start'"
      >
        <div
          v-if="msg.role === 'assistant'"
          class="w-10 h-10 bg-orange-400 rounded-full flex items-center justify-center text-lg mr-2 flex-shrink-0"
        >
          🤖
        </div>
        <div
          class="max-w-[75%] px-4 py-3 rounded-2xl"
          :class="msg.role === 'user' 
            ? 'bg-orange-400 text-white rounded-br-sm' 
            : 'bg-white text-gray-800 rounded-bl-sm shadow-sm'"
        >
          <p class="text-base leading-relaxed">{{ msg.content }}</p>
        </div>
        <div
          v-if="msg.role === 'user'"
          class="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center text-lg ml-2 flex-shrink-0"
        >
          👵
        </div>
      </div>

      <div v-if="isTyping" class="mb-4 flex justify-start">
        <div class="w-10 h-10 bg-orange-400 rounded-full flex items-center justify-center text-lg mr-2 flex-shrink-0">
          🤖
        </div>
        <div class="bg-white px-4 py-3 rounded-2xl rounded-bl-sm shadow-sm">
          <div class="flex gap-1">
            <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
            <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
            <span class="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
          </div>
        </div>
      </div>
    </div>

    <div class="px-4 py-3 bg-white border-t border-gray-100">
      <div class="flex gap-2 mb-2 overflow-x-auto pb-1">
        <button
          v-for="phrase in quickPhrases"
          :key="phrase"
          @click="sendQuickPhrase(phrase)"
          class="flex-shrink-0 px-3 py-1.5 bg-orange-50 text-orange-600 rounded-full text-sm hover:bg-orange-100 active:scale-95 transition-all"
        >
          {{ phrase }}
        </button>
      </div>
      <div class="flex gap-2 items-end">
        <input
          v-model="inputMessage"
          @keyup.enter="handleSend"
          type="text"
          placeholder="想说点什么..."
          class="flex-1 px-4 py-3 bg-gray-100 rounded-2xl text-base focus:outline-none focus:ring-2 focus:ring-orange-300"
        />
        <button
          @click="handleSend"
          :disabled="!inputMessage.trim() || isTyping"
          class="w-12 h-12 bg-gradient-to-r from-orange-400 to-amber-500 text-white rounded-full flex items-center justify-center text-xl disabled:opacity-50 active:scale-95 transition-all"
        >
          📤
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue'
import { useUserStore } from '../../stores/user'
import { sendMessage, getChatHistory } from '../../api/chat'

const userStore = useUserStore()
const messages = ref<any[]>([])
const inputMessage = ref('')
const isTyping = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)

const quickPhrases = [
  '你好呀',
  '今天天气怎么样',
  '我有点不舒服',
  '给我讲个笑话',
  '提醒我吃药'
]

const elderUserId = computed(() => userStore.userInfo?.id)

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

async function loadHistory() {
  if (!elderUserId.value) return
  try {
    const res: any = await getChatHistory(elderUserId.value)
    messages.value = res.messages || []
    scrollToBottom()
  } catch (error) {
    console.error('加载聊天记录失败', error)
  }
}

async function handleSend() {
  const text = inputMessage.value.trim()
  if (!text || isTyping.value || !elderUserId.value) return

  const userMsg: any = {
    id: Date.now(),
    role: 'user',
    content: text
  }
  messages.value.push(userMsg)
  inputMessage.value = ''
  isTyping.value = true
  scrollToBottom()

  try {
    const res: any = await sendMessage(elderUserId.value, text)
    isTyping.value = false
    messages.value.push(res)
    scrollToBottom()
  } catch (error) {
    console.error('发送消息失败', error)
    isTyping.value = false
    messages.value.push({
      id: Date.now() + 1,
      role: 'assistant',
      content: '抱歉，我现在有点累，等会儿再聊好吗？'
    })
    scrollToBottom()
  }
}

function sendQuickPhrase(phrase: string) {
  inputMessage.value = phrase
  handleSend()
}

onMounted(() => {
  loadHistory()
})
</script>
