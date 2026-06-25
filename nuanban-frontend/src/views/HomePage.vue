<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-100 flex flex-col items-center justify-center p-6">
    <!-- Logo -->
    <div class="mb-8 text-center">
      <div class="w-24 h-24 bg-gradient-to-br from-orange-400 to-amber-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-lg">
        <span class="text-5xl">🤖</span>
      </div>
      <h1 class="text-3xl font-bold text-gray-800">暖伴</h1>
      <p class="text-gray-500 mt-2">智能陪伴，温暖守护</p>
    </div>

    <!-- 角色选择 -->
    <div class="w-full max-w-sm space-y-4">
      <button
        @click="goToLogin('elder')"
        class="w-full p-6 bg-white rounded-2xl shadow-md hover:shadow-lg transition-all flex items-center gap-4 border-2 border-transparent hover:border-orange-300"
      >
        <div class="w-14 h-14 bg-orange-100 rounded-full flex items-center justify-center text-3xl">
          👵
        </div>
        <div class="text-left flex-1">
          <h2 class="text-xl font-semibold text-gray-800">我是老人</h2>
          <p class="text-gray-500 text-sm">陪伴聊天 · 用药提醒 · 紧急求助</p>
        </div>
        <span class="text-orange-400 text-2xl">→</span>
      </button>

      <button
        @click="goToLogin('child')"
        class="w-full p-6 bg-white rounded-2xl shadow-md hover:shadow-lg transition-all flex items-center gap-4 border-2 border-transparent hover:border-orange-300"
      >
        <div class="w-14 h-14 bg-amber-100 rounded-full flex items-center justify-center text-3xl">
          👨‍👩‍👧
        </div>
        <div class="text-left flex-1">
          <h2 class="text-xl font-semibold text-gray-800">我是子女</h2>
          <p class="text-gray-500 text-sm">查看状态 · 异常提醒 · 健康报告</p>
        </div>
        <span class="text-orange-400 text-2xl">→</span>
      </button>
    </div>

    <!-- 底部 -->
    <p class="mt-12 text-gray-400 text-sm">
      用科技守护每一位长辈
    </p>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function goToLogin(role: string) {
  router.push({ path: '/login', query: { role } })
}
</script>