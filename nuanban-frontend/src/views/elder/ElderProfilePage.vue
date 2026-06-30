<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-orange-400 to-amber-500 text-white p-6 pt-10 pb-16 rounded-b-3xl">
      <div class="flex items-center gap-4">
        <div class="w-20 h-20 bg-white/20 rounded-full flex items-center justify-center text-4xl">
          👵
        </div>
        <div>
          <h1 class="text-2xl font-bold">{{ profile?.real_name || userStore.userInfo?.username }}</h1>
          <p class="text-orange-100 mt-1">{{ userStore.userInfo?.phone || '暂无手机号' }}</p>
        </div>
      </div>
    </div>

    <!-- 个人信息卡片 -->
    <div class="px-4 -mt-8">
      <div class="bg-white rounded-2xl shadow-md overflow-hidden">
        <div class="p-4 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-800">基本信息</h2>
        </div>
        <div class="divide-y divide-gray-100">
          <div class="p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-xl">👤</span>
              <span class="text-gray-600">姓名</span>
            </div>
            <span class="text-gray-800">{{ profile?.real_name || userStore.userInfo?.username }}</span>
          </div>
          <div class="p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-xl">⚧</span>
              <span class="text-gray-600">性别</span>
            </div>
            <span class="text-gray-800">{{ profile?.gender || '未设置' }}</span>
          </div>
          <div class="p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-xl">🎂</span>
              <span class="text-gray-600">年龄</span>
            </div>
            <span class="text-gray-800">{{ profile?.age || '未设置' }}岁</span>
          </div>
          <div class="p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-xl">📱</span>
              <span class="text-gray-600">手机号</span>
            </div>
            <span class="text-gray-800">{{ userStore.userInfo?.phone || '未设置' }}</span>
          </div>
          <div class="p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-xl">🏠</span>
              <span class="text-gray-600">住址</span>
            </div>
            <span class="text-gray-800">{{ profile?.address || '未设置' }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- 紧急联系人卡片 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-2xl shadow-md overflow-hidden">
        <div class="p-4 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-800">紧急联系人</h2>
        </div>
        <div class="divide-y divide-gray-100">
          <div class="p-4 flex items-center justify-between">
            <div class="flex items-center gap-3">
              <span class="text-xl">👨</span>
              <span class="text-gray-600">联系人</span>
            </div>
            <span class="text-gray-800">{{ profile?.emergency_contact || '未设置' }}</span>
          </div>
          <div class="p-4 flex items-center justify-between cursor-pointer" @click="callEmergency">
            <div class="flex items-center gap-3">
              <span class="text-xl">📞</span>
              <span class="text-gray-600">联系电话</span>
            </div>
            <span class="text-orange-500 flex items-center gap-1">
              {{ profile?.emergency_phone || '未设置' }}
              <span v-if="profile?.emergency_phone" class="text-lg">📱</span>
            </span>
          </div>
        </div>
      </div>
    </div>

    <!-- 功能列表 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-2xl shadow-md overflow-hidden">
        <div class="p-4 flex items-center justify-between cursor-pointer hover:bg-gray-50 transition-colors" @click="showChangePassword = true">
          <div class="flex items-center gap-3">
            <span class="text-xl">🔑</span>
            <span class="text-gray-800">修改密码</span>
          </div>
          <span class="text-gray-400">›</span>
        </div>
        <div class="p-4 flex items-center justify-between cursor-pointer hover:bg-gray-50 transition-colors border-t border-gray-100" @click="handleLogout">
          <div class="flex items-center gap-3">
            <span class="text-xl">🚪</span>
            <span class="text-red-500">退出登录</span>
          </div>
          <span class="text-gray-400">›</span>
        </div>
      </div>
    </div>

    <!-- 版本信息 -->
    <div class="px-4 mt-6 text-center">
      <p class="text-gray-400 text-sm">暖伴 v1.0.0</p>
    </div>

    <!-- 修改密码弹窗 -->
    <div v-if="showChangePassword" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div class="bg-white rounded-2xl w-full max-w-sm p-6">
        <h3 class="text-xl font-bold text-gray-800 mb-6">修改密码</h3>
        <div class="space-y-4">
          <div>
            <label class="block text-sm text-gray-600 mb-1">原密码</label>
            <input
              v-model="passwordForm.oldPassword"
              type="password"
              placeholder="请输入原密码"
              class="w-full px-4 py-3 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-300"
            />
          </div>
          <div>
            <label class="block text-sm text-gray-600 mb-1">新密码</label>
            <input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="请输入新密码"
              class="w-full px-4 py-3 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-300"
            />
          </div>
          <div>
            <label class="block text-sm text-gray-600 mb-1">确认新密码</label>
            <input
              v-model="passwordForm.confirmPassword"
              type="password"
              placeholder="请再次输入新密码"
              class="w-full px-4 py-3 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-orange-300"
            />
          </div>
        </div>
        <div class="flex gap-3 mt-6">
          <button
            @click="showChangePassword = false"
            class="flex-1 py-3 bg-gray-100 text-gray-600 rounded-xl"
          >
            取消
          </button>
          <button
            @click="handleChangePassword"
            :disabled="isChangingPassword"
            class="flex-1 py-3 bg-gradient-to-r from-orange-400 to-amber-500 text-white rounded-xl disabled:opacity-50"
          >
            {{ isChangingPassword ? '修改中...' : '确认' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { changePassword, getCurrentUser } from '../../api/auth'
import { getElderProfile } from '../../api/family'

const router = useRouter()
const userStore = useUserStore()

const profile = ref<any>(null)
const showChangePassword = ref(false)
const isChangingPassword = ref(false)

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

async function loadData() {
  try {
    // 获取当前用户信息
    const userRes: any = await getCurrentUser()
    userStore.setUserInfo(userRes)

    // 获取老人档案
    if (userStore.userInfo?.id) {
      try {
        const profileRes: any = await getElderProfile(userStore.userInfo.id)
        profile.value = profileRes
      } catch (e) {
        // 档案不存在，忽略
        console.log('暂无老人档案')
      }
    }
  } catch (error) {
    console.error('加载数据失败', error)
  }
}

function callEmergency() {
  if (profile.value?.emergency_phone) {
    window.location.href = `tel:${profile.value.emergency_phone}`
  }
}

async function handleChangePassword() {
  if (!passwordForm.value.oldPassword) {
    alert('请输入原密码')
    return
  }
  if (!passwordForm.value.newPassword) {
    alert('请输入新密码')
    return
  }
  if (passwordForm.value.newPassword !== passwordForm.value.confirmPassword) {
    alert('两次输入的新密码不一致')
    return
  }
  if (passwordForm.value.newPassword.length < 6) {
    alert('新密码长度不能少于6位')
    return
  }

  isChangingPassword.value = true
  try {
    await changePassword(passwordForm.value.oldPassword, passwordForm.value.newPassword)
    alert('密码修改成功！')
    showChangePassword.value = false
    passwordForm.value = { oldPassword: '', newPassword: '', confirmPassword: '' }
  } catch (error: any) {
    alert(error.response?.data?.detail || '修改失败，请检查原密码是否正确')
  } finally {
    isChangingPassword.value = false
  }
}

function handleLogout() {
  if (confirm('确定要退出登录吗？')) {
    userStore.logout()
    router.push({ path: '/login', query: { role: 'elder' } })
  }
}

onMounted(() => {
  loadData()
})
</script>
