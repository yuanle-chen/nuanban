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
          <h2 class="text-xl font-bold">{{ currentElder?.profile?.real_name || currentElder?.username || '加载中...' }}</h2>
          <p class="text-white/80 text-sm">{{ currentElder?.relation_type || '子女' }}</p>
        </div>
      </div>
    </div>

    <!-- 档案表单 -->
    <div class="px-4 -mt-8">
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
import { ref, computed, onMounted } from 'vue'
import { useFamilyStore } from '../../stores/family'
import { createElderProfile, updateElderProfile, getElderProfile } from '../../api/family'

const familyStore = useFamilyStore()
const currentElder = computed(() => familyStore.currentElder)

const loading = ref(false)
const form = ref({
  real_name: '',
  age: undefined as number | undefined,
  gender: '',
  address: '',
  emergency_contact: '',
  emergency_phone: '',
})

onMounted(async () => {
  if (!currentElder.value) {
    await familyStore.fetchElders()
  }
  if (currentElder.value?.profile) {
    form.value = {
      real_name: currentElder.value.profile.real_name || '',
      age: currentElder.value.profile.age,
      gender: currentElder.value.profile.gender || '',
      address: currentElder.value.profile.address || '',
      emergency_contact: currentElder.value.profile.emergency_contact || '',
      emergency_phone: currentElder.value.profile.emergency_phone || '',
    }
  }
})

async function handleSave() {
  if (!form.value.real_name) {
    alert('请输入真实姓名')
    return
  }
  if (!currentElder.value) {
    alert('请先绑定老人')
    return
  }

  loading.value = true
  try {
    if (currentElder.value.profile) {
      await updateElderProfile(currentElder.value.id, form.value)
    } else {
      await createElderProfile({
        user_id: currentElder.value.id,
        ...form.value,
      })
    }
    alert('保存成功！')
    await familyStore.fetchElders()
  } catch (err: any) {
    alert(err.response?.data?.detail || '保存失败')
  } finally {
    loading.value = false
  }
}
</script>