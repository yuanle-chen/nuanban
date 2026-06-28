<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <div class="bg-gradient-to-r from-blue-500 to-cyan-400 text-white p-6 pb-20">
      <div class="flex items-center gap-3 mb-4">
        <button @click="$router.back()" class="text-white text-lg">← 返回</button>
        <h1 class="text-xl font-bold">老人档案</h1>
      </div>
      <div class="flex items-center gap-4 mt-4">
        <div class="w-16 h-16 bg-white/20 rounded-full flex items-center justify-center text-3xl">
          👴
        </div>
        <div>
          <h2 class="text-xl font-bold">{{ elderInfo?.profile?.real_name || elderInfo?.username || '加载中...' }}</h2>
          <p class="text-white/80 text-sm">{{ elderInfo?.phone || '' }}</p>
        </div>
      </div>
    </div>

    <!-- 档案表单 -->
    <div class="px-4 -mt-8 pb-8">
      <div class="bg-white rounded-2xl p-6 shadow-lg">
        <div class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">真实姓名 *</label>
            <input
              v-model="form.real_name"
              type="text"
              placeholder="请输入真实姓名"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">年龄</label>
              <input
                v-model.number="form.age"
                type="number"
                placeholder="年龄"
                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">性别</label>
              <select
                v-model="form.gender"
                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
              >
                <option value="">请选择</option>
                <option value="男">男</option>
                <option value="女">女</option>
              </select>
            </div>
          </div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">住址</label>
            <input
              v-model="form.address"
              type="text"
              placeholder="请输入住址"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
            />
          </div>

          <div class="pt-4 border-t">
            <h3 class="font-semibold text-gray-800 mb-4">紧急联系人</h3>
            <div class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">紧急联系人姓名</label>
                <input
                  v-model="form.emergency_contact"
                  type="text"
                  placeholder="请输入紧急联系人姓名"
                  class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-gray-700 mb-1">紧急联系电话</label>
                <input
                  v-model="form.emergency_phone"
                  type="tel"
                  placeholder="请输入紧急联系电话"
                  class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
                />
              </div>
            </div>
          </div>

          <button
            @click="handleSave"
            :disabled="loading"
            class="w-full py-3 bg-gradient-to-r from-blue-500 to-cyan-400 text-white font-semibold rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {{ loading ? '保存中...' : '保存档案' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useFamilyStore } from '../../stores/family'
import { createElderProfile, updateElderProfile, getElderProfile } from '../../api/family'

const route = useRoute()
const router = useRouter()
const familyStore = useFamilyStore()

const loading = ref(false)
const elderInfo = ref<any>(null)
const hasProfile = ref(false)

const form = ref({
  real_name: '',
  age: undefined as number | undefined,
  gender: '',
  address: '',
  emergency_contact: '',
  emergency_phone: '',
})

const elderUserId = computed(() => {
  const id = route.query.id
  if (id) return Number(id)
  return familyStore.currentElder?.id
})

async function loadElderInfo() {
  if (!elderUserId.value) return

  // 尝试从 familyStore 中找老人信息
  let elder = familyStore.elders.find((e: any) => e.id === elderUserId.value)
  if (elder) {
    elderInfo.value = elder
  } else {
    // 如果找不到，先拉取列表
    await familyStore.fetchElders()
    elder = familyStore.elders.find((e: any) => e.id === elderUserId.value)
    if (elder) {
      elderInfo.value = elder
    }
  }

  // 加载档案
  try {
    const profile: any = await getElderProfile(elderUserId.value)
    hasProfile.value = true
    form.value = {
      real_name: profile.real_name || '',
      age: profile.age,
      gender: profile.gender || '',
      address: profile.address || '',
      emergency_contact: profile.emergency_contact || '',
      emergency_phone: profile.emergency_phone || '',
    }
    // 更新 elderInfo 的 profile
    if (elderInfo.value) {
      elderInfo.value.profile = profile
    }
  } catch (e) {
    hasProfile.value = false
    // 档案不存在，用老人的用户名作为默认姓名
    if (elderInfo.value) {
      form.value.real_name = elderInfo.value.username || ''
    }
  }
}

async function handleSave() {
  if (!form.value.real_name) {
    alert('请输入真实姓名')
    return
  }
  if (!elderUserId.value) {
    alert('缺少老人ID')
    return
  }

  loading.value = true
  try {
    if (hasProfile.value) {
      await updateElderProfile(elderUserId.value, form.value)
    } else {
      await createElderProfile({
        user_id: elderUserId.value,
        ...form.value,
      })
    }
    alert('保存成功！')
    await familyStore.fetchElders()
    router.back()
  } catch (err: any) {
    alert(err.response?.data?.detail || '保存失败')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadElderInfo()
})
</script>
