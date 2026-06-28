<template>
  <div class="min-h-screen bg-gray-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-blue-500 to-cyan-500 text-white p-6 pt-10 pb-16 rounded-b-3xl">
      <div class="flex items-center gap-4">
        <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-3xl">
          👨
        </div>
        <div>
          <h1 class="text-xl font-bold">{{ userStore.userInfo?.username }}</h1>
          <p class="text-blue-100 text-sm mt-1">{{ userStore.userInfo?.phone || '暂无手机号' }}</p>
        </div>
      </div>
    </div>

    <!-- 已绑定的老人 -->
    <div class="px-4 -mt-8">
      <div class="bg-white rounded-2xl shadow-md overflow-hidden">
        <div class="p-4 border-b border-gray-100 flex items-center justify-between">
          <h2 class="text-lg font-semibold text-gray-800">已绑定的老人</h2>
          <button
            @click="goTo('/child/bind')"
            class="text-blue-500 text-sm"
          >
            + 添加
          </button>
        </div>
        <div v-if="elders.length === 0" class="p-8 text-center text-gray-400">
          <p class="text-3xl mb-2">👵</p>
          <p>暂无绑定的老人</p>
          <button
            @click="goTo('/child/bind')"
            class="mt-3 px-4 py-2 bg-blue-500 text-white rounded-full text-sm"
          >
            立即绑定
          </button>
        </div>
        <div v-else class="divide-y divide-gray-100">
          <div
            v-for="elder in elders"
            :key="elder.id"
            class="p-4 flex items-center justify-between"
          >
            <div class="flex items-center gap-3 cursor-pointer" @click="goToProfile(elder)">
              <div class="w-12 h-12 bg-orange-100 rounded-full flex items-center justify-center text-xl">
                👵
              </div>
              <div>
                <p class="font-medium text-gray-800">
                  {{ elder.profile?.real_name || elder.username }}
                </p>
                <p class="text-sm text-gray-400">{{ elder.relation_type }} · {{ elder.phone }}</p>
              </div>
            </div>
            <div class="flex items-center gap-2">
              <button
                v-if="currentElderId !== elder.id"
                @click="switchElder(elder)"
                class="px-3 py-1 bg-blue-50 text-blue-500 rounded-full text-sm"
              >
                切换
              </button>
              <span
                v-else
                class="px-3 py-1 bg-green-50 text-green-500 rounded-full text-sm"
              >
                当前
              </span>
              <button
                @click="handleUnbind(elder)"
                class="px-3 py-1 bg-red-50 text-red-500 rounded-full text-sm"
              >
                解绑
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 通知设置 -->
    <div class="px-4 mt-4">
      <div class="bg-white rounded-2xl shadow-md overflow-hidden">
        <div class="p-4 border-b border-gray-100">
          <h2 class="text-lg font-semibold text-gray-800">通知设置</h2>
        </div>
        <div class="p-4 flex items-center justify-between">
          <div class="flex items-center gap-3">
            <span class="text-xl">🆘</span>
            <div>
              <p class="text-gray-800">紧急求助提醒</p>
              <p class="text-xs text-gray-400">老人发起SOS时推送通知</p>
            </div>
          </div>
          <div
            @click="notifySettings.emergency = !notifySettings.emergency"
            class="w-12 h-7 rounded-full cursor-pointer transition-colors"
            :class="notifySettings.emergency ? 'bg-blue-500' : 'bg-gray-300'"
          >
            <div
              class="w-5 h-5 bg-white rounded-full shadow-sm transition-transform mt-1"
              :class="notifySettings.emergency ? 'ml-6' : 'ml-1'"
            ></div>
          </div>
        </div>
        <div class="p-4 flex items-center justify-between border-t border-gray-100">
          <div class="flex items-center gap-3">
            <span class="text-xl">💊</span>
            <div>
              <p class="text-gray-800">用药提醒</p>
              <p class="text-xs text-gray-400">老人未按时服药时推送提醒</p>
            </div>
          </div>
          <div
            @click="notifySettings.medication = !notifySettings.medication"
            class="w-12 h-7 rounded-full cursor-pointer transition-colors"
            :class="notifySettings.medication ? 'bg-blue-500' : 'bg-gray-300'"
          >
            <div
              class="w-5 h-5 bg-white rounded-full shadow-sm transition-transform mt-1"
              :class="notifySettings.medication ? 'ml-6' : 'ml-1'"
            ></div>
          </div>
        </div>
        <div class="p-4 flex items-center justify-between border-t border-gray-100">
          <div class="flex items-center gap-3">
            <span class="text-xl">❤️</span>
            <div>
              <p class="text-gray-800">健康异常提醒</p>
              <p class="text-xs text-gray-400">健康数据异常时推送提醒</p>
            </div>
          </div>
          <div
            @click="notifySettings.health = !notifySettings.health"
            class="w-12 h-7 rounded-full cursor-pointer transition-colors"
            :class="notifySettings.health ? 'bg-blue-500' : 'bg-gray-300'"
          >
            <div
              class="w-5 h-5 bg-white rounded-full shadow-sm transition-transform mt-1"
              :class="notifySettings.health ? 'ml-6' : 'ml-1'"
            ></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 账户设置 -->
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
              class="w-full px-4 py-3 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>
          <div>
            <label class="block text-sm text-gray-600 mb-1">新密码</label>
            <input
              v-model="passwordForm.newPassword"
              type="password"
              placeholder="请输入新密码"
              class="w-full px-4 py-3 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>
          <div>
            <label class="block text-sm text-gray-600 mb-1">确认新密码</label>
            <input
              v-model="passwordForm.confirmPassword"
              type="password"
              placeholder="请再次输入新密码"
              class="w-full px-4 py-3 bg-gray-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
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
            class="flex-1 py-3 bg-gradient-to-r from-blue-500 to-cyan-500 text-white rounded-xl disabled:opacity-50"
          >
            {{ isChangingPassword ? '修改中...' : '确认' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '../../stores/user'
import { useFamilyStore } from '../../stores/family'
import { getCurrentUser, changePassword } from '../../api/auth'
import { getMyElders, unbindElder } from '../../api/family'

const router = useRouter()
const userStore = useUserStore()
const familyStore = useFamilyStore()

const elders = ref<any[]>([])
const showChangePassword = ref(false)
const isChangingPassword = ref(false)

const defaultSettings = {
  emergency: true,
  medication: true,
  health: true
}

function loadNotifySettings() {
  const saved = localStorage.getItem('notifySettings')
  if (saved) {
    try {
      return { ...defaultSettings, ...JSON.parse(saved) }
    } catch (e) {
      return { ...defaultSettings }
    }
  }
  return { ...defaultSettings }
}

const notifySettings = ref(loadNotifySettings())

watch(notifySettings, (val) => {
  localStorage.setItem('notifySettings', JSON.stringify(val))
}, { deep: true })

const passwordForm = ref({
  oldPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const currentElderId = computed(() => familyStore.currentElder?.id)

async function loadData() {
  try {
    const userRes: any = await getCurrentUser()
    userStore.setUserInfo(userRes)

    await familyStore.fetchElders()
    elders.value = familyStore.elders
  } catch (error) {
    console.error('加载数据失败', error)
  }
}

function goTo(path: string) {
  router.push(path)
}

function goToProfile(elder: any) {
  router.push({ path: '/child/profile', query: { id: elder.id } })
}

function switchElder(elder: any) {
  familyStore.setCurrentElder(elder)
  router.push('/child')
}

async function handleUnbind(elder: any) {
  if (!confirm(`确定要解绑 ${elder.profile?.real_name || elder.username} 吗？`)) return

  try {
    await unbindElder(elder.id)
    alert('解绑成功')
    await familyStore.fetchElders()
    elders.value = familyStore.elders
  } catch (error: any) {
    alert(error.response?.data?.detail || '解绑失败')
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
    familyStore.$reset()
    router.push('/login')
  }
}

onMounted(() => {
  loadData()
})
</script>
