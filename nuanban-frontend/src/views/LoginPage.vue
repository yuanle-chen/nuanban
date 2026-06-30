<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-100 flex flex-col items-center justify-center p-6">
    <div class="w-full max-w-sm">
      <!-- 返回 -->
      <button @click="$router.back()" class="mb-6 text-gray-500 hover:text-gray-700 flex items-center gap-1">
        ← 返回
      </button>

      <!-- 标题 -->
      <div class="text-center mb-8">
        <h1 class="text-2xl font-bold text-gray-800">
          {{ role === 'elder' ? '老人登录' : '子女登录' }}
        </h1>
        <p class="text-gray-500 mt-2">欢迎回到暖伴</p>
      </div>

      <!-- 表单 -->
      <div class="bg-white rounded-2xl p-6 shadow-md space-y-4">
        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">用户名</label>
          <input
            v-model="form.username"
            type="text"
            placeholder="请输入用户名"
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-transparent"
          />
        </div>

        <div>
          <label class="block text-sm font-medium text-gray-700 mb-1">密码</label>
          <input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-300 focus:border-transparent"
          />
        </div>

        <button
          @click="handleLogin"
          :disabled="loading"
          class="w-full py-3 bg-gradient-to-r from-orange-400 to-amber-500 text-white font-semibold rounded-xl hover:from-orange-500 hover:to-amber-600 transition-all disabled:opacity-50"
        >
          {{ loading ? '登录中...' : '登 录' }}
        </button>

        <div class="flex justify-between items-center text-sm">
          <span></span>
          <button @click="goToForgotPassword" class="text-orange-500 hover:text-orange-600">
            忘记密码？
          </button>
        </div>

        <div class="text-center text-sm text-gray-500">
          还没有账号？
          <button @click="goToRegister" class="text-orange-500 hover:text-orange-600 font-medium">
            立即注册
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '../stores/user'
import { login, getCurrentUser } from '../api/auth'
import { speak } from '../utils/speech'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const form = ref({
  username: '',
  password: ''
})
const loading = ref(false)

const role = computed(() => route.query.role || 'elder')

async function handleLogin() {
  if (!form.value.username || !form.value.password) {
    alert('请输入用户名和密码')
    return
  }

  loading.value = true
  try {
    const res: any = await login(form.value.username, form.value.password)
    
    if (res.role !== role.value) {
      userStore.logout()
      const roleName = res.role === 'elder' ? '老人' : '子女'
      const entryName = role.value === 'elder' ? '老人' : '子女'
      alert(`该账号是${roleName}账号，请从${entryName}端登录`)
      loading.value = false
      return
    }
    
    userStore.setToken(res.access_token, role.value as string)
    
    const userRes: any = await getCurrentUser()
    userStore.setUserInfo(userRes)
    
    if (role.value === 'elder') {
      router.push('/elder')
      setTimeout(() => {
        const hour = new Date().getHours()
        let greeting = '晚上好'
        if (hour < 6) greeting = '夜深了，注意休息'
        else if (hour < 12) greeting = '早上好'
        else if (hour < 14) greeting = '中午好'
        else if (hour < 18) greeting = '下午好'
        speak(`${greeting}，${userRes.username || '老人家'}，欢迎回来`)
      }, 500)
    } else {
      router.push('/child')
    }
  } catch (err: any) {
    alert(err.response?.data?.detail || '登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}

function goToRegister() {
  router.push({ path: '/register', query: { role: role.value } })
}

function goToForgotPassword() {
  router.push('/forgot-password')
}
</script>