<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <div class="bg-gradient-to-r from-blue-500 to-cyan-400 text-white p-6 pb-20">
      <div class="flex items-center gap-3 mb-4">
        <button @click="$router.back()" class="text-white text-lg">← 返回</button>
        <h1 class="text-xl font-bold">绑定老人</h1>
      </div>
    </div>

    <!-- 表单卡片 -->
    <div class="px-4 -mt-12">
      <div class="bg-white rounded-2xl p-6 shadow-lg">
        <div class="text-center mb-6">
          <div class="text-5xl mb-2">👴</div>
          <p class="text-gray-600">输入老人的手机号进行绑定</p>
        </div>

        <div class="space-y-4">
          <div>
  <label class="block text-sm font-medium text-gray-700 mb-1">老人手机号</label>
  <input
    v-model="elderPhone"
    type="tel"
    placeholder="请输入老人的手机号"
    class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
  />
</div>

          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">关系</label>
            <select
              v-model="relationType"
              class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-300"
            >
              <option value="子女">子女</option>
              <option value="儿子">儿子</option>
              <option value="女儿">女儿</option>
              <option value="儿媳">儿媳</option>
              <option value="女婿">女婿</option>
              <option value="其他亲属">其他亲属</option>
            </select>
          </div>

          <button
            @click="handleBind"
            :disabled="loading"
            class="w-full py-3 bg-gradient-to-r from-blue-500 to-cyan-400 text-white font-semibold rounded-xl hover:opacity-90 transition-opacity disabled:opacity-50"
          >
            {{ loading ? '绑定中...' : '立即绑定' }}
          </button>
        </div>

        <div class="mt-6 p-4 bg-blue-50 rounded-xl">
  <p class="text-sm text-blue-700">
    💡 提示：请输入老人注册时使用的手机号进行绑定。
  </p>
</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { bindElderByPhone } from '../../api/family'
import { useFamilyStore } from '../../stores/family'

const router = useRouter()
const familyStore = useFamilyStore()

const elderPhone = ref('')
const relationType = ref('子女')
const loading = ref(false)

async function handleBind() {
  if (!elderPhone.value) {
    alert('请输入老人手机号')
    return
  }
  if (!/^1[3-9]\d{9}$/.test(elderPhone.value)) {
    alert('请输入正确的手机号')
    return
  }

  loading.value = true
  try {
    await bindElderByPhone(elderPhone.value, relationType.value)
    alert('绑定成功！')
    await familyStore.fetchElders()
    router.back()
  } catch (err: any) {
    alert(err.response?.data?.detail || '绑定失败')
  } finally {
    loading.value = false
  }
}
</script>