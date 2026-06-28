<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-400 to-amber-500 flex flex-col">
    <!-- 顶部 -->
    <div class="p-6 pt-12">
      <button @click="$router.back()" class="text-white text-lg flex items-center gap-2">
        <span>←</span> 返回
      </button>
    </div>

    <!-- 表单区域 -->
    <div class="flex-1 px-6 pb-8">
      <div class="bg-white rounded-t-3xl rounded-b-3xl p-8 shadow-2xl min-h-[60vh]">
        <div class="text-center mb-8">
          <div class="text-5xl mb-4">🔑</div>
          <h1 class="text-2xl font-bold text-gray-800">找回密码</h1>
          <p class="text-gray-500 mt-2">通过手机验证码重置密码</p>
        </div>

        <!-- 步骤1：输入手机号 -->
        <div v-if="step === 1" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">手机号</label>
            <input
              v-model="phone"
              type="tel"
              placeholder="请输入注册时的手机号"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-300"
            />
          </div>

          <button
            @click="handleSendCode"
            :disabled="countdown > 0"
            class="w-full py-3 bg-gradient-to-r from-orange-400 to-amber-500 text-white font-semibold rounded-xl disabled:opacity-50"
          >
            {{ countdown > 0 ? `${countdown}秒后可重新发送` : '发送验证码' }}
          </button>

          <!-- 开发测试模式：显示验证码 -->
          <div v-if="devCode" class="p-4 bg-yellow-50 rounded-xl text-center">
            <p class="text-yellow-700 text-sm">【开发测试】验证码：<span class="font-bold text-lg">{{ devCode }}</span></p>
          </div>
        </div>

        <!-- 步骤2：输入验证码和新密码 -->
        <div v-if="step === 2" class="space-y-4">
          <div class="p-4 bg-green-50 rounded-xl">
            <p class="text-green-700 text-sm">验证码已发送至 <span class="font-medium">{{ phone }}</span></p>
          </div>

          <!-- 开发测试模式：显示验证码 -->
          <div v-if="devCode" class="p-4 bg-yellow-50 rounded-xl text-center">
            <p class="text-yellow-700 text-sm">【开发测试】验证码：<span class="font-bold text-lg">{{ devCode }}</span></p>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">验证码</label>
            <div class="flex gap-2">
              <input
                v-model="code"
                type="text"
                maxlength="6"
                placeholder="请输入6位验证码"
                class="flex-1 px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-300"
              />
              <button
                @click="handleSendCode"
                :disabled="countdown > 0"
                class="px-4 py-3 bg-gray-100 text-gray-600 rounded-xl disabled:opacity-50 text-sm"
              >
                {{ countdown > 0 ? `${countdown}s` : '重发' }}
              </button>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">新密码</label>
            <input
              v-model="newPassword"
              type="password"
              placeholder="请输入新密码（至少6位）"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-300"
            />
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">确认新密码</label>
            <input
              v-model="confirmPassword"
              type="password"
              placeholder="请再次输入新密码"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-300"
            />
          </div>

          <button
            @click="handleReset"
            :disabled="loading"
            class="w-full py-3 bg-gradient-to-r from-orange-400 to-amber-500 text-white font-semibold rounded-xl disabled:opacity-50"
          >
            {{ loading ? '重置中...' : '重置密码' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { sendCode, resetPassword } from '../api/auth'

const router = useRouter()

const step = ref(1)
const phone = ref('')
const code = ref('')
const newPassword = ref('')
const confirmPassword = ref('')
const loading = ref(false)
const countdown = ref(0)
const devCode = ref('')

let countdownTimer: ReturnType<typeof setInterval> | null = null

function startCountdown() {
  countdown.value = 60
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      if (countdownTimer) clearInterval(countdownTimer)
    }
  }, 1000)
}

async function handleSendCode() {
  if (!phone.value) {
    alert('请输入手机号')
    return
  }
  if (!/^1[3-9]\d{9}$/.test(phone.value)) {
    alert('请输入正确的手机号')
    return
  }

  try {
    const res: any = await sendCode(phone.value)
    step.value = 2
    devCode.value = res.code || ''
    startCountdown()
  } catch (err: any) {
    alert(err.response?.data?.detail || '发送失败')
  }
}

async function handleReset() {
  if (!code.value) {
    alert('请输入验证码')
    return
  }
  if (code.value.length !== 6) {
    alert('验证码为6位数字')
    return
  }
  if (!newPassword.value) {
    alert('请输入新密码')
    return
  }
  if (newPassword.value.length < 6) {
    alert('密码长度不能少于6位')
    return
  }
  if (newPassword.value !== confirmPassword.value) {
    alert('两次输入的密码不一致')
    return
  }

  loading.value = true
  try {
    await resetPassword(phone.value, code.value, newPassword.value)
    alert('密码重置成功！请使用新密码登录')
    router.replace('/login')
  } catch (err: any) {
    alert(err.response?.data?.detail || '重置失败')
  } finally {
    loading.value = false
  }
}
</script>
