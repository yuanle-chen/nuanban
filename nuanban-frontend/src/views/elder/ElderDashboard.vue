<template>
  <div class="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50 pb-20">
    <!-- 顶部 -->
    <div class="bg-gradient-to-r from-orange-400 to-amber-500 text-white p-6 pt-10 pb-16 rounded-b-3xl">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-orange-100 text-sm">早上好</p>
          <h1 class="text-2xl font-bold mt-1">李奶奶 👋</h1>
        </div>
        <div class="w-12 h-12 bg-white/20 rounded-full flex items-center justify-center text-2xl">
          👵
        </div>
      </div>
    </div>

    <!-- 健康卡片 -->
    <div class="px-4 -mt-8">
      <div class="bg-white rounded-2xl p-5 shadow-md">
        <h2 class="text-lg font-semibold text-gray-800 mb-4">今日健康</h2>
        <div class="grid grid-cols-2 gap-4">
          <div class="bg-red-50 rounded-xl p-4 text-center">
            <p class="text-2xl font-bold text-red-500">120/80</p>
            <p class="text-sm text-gray-500 mt-1">血压 mmHg</p>
          </div>
          <div class="bg-orange-50 rounded-xl p-4 text-center">
            <p class="text-2xl font-bold text-orange-500">72</p>
            <p class="text-sm text-gray-500 mt-1">心率 次/分</p>
          </div>
        </div>
      </div>
    </div>

    <!-- 快捷功能 -->
    <div class="px-4 mt-6">
      <h2 class="text-lg font-semibold text-gray-800 mb-4">常用功能</h2>
      <div class="grid grid-cols-2 gap-4">
        <div
          v-for="item in features"
          :key="item.name"
          @click="goTo(item.path)"
          class="bg-white rounded-2xl p-5 shadow-md hover:shadow-lg transition-all cursor-pointer active:scale-95"
        >
          <div class="text-4xl mb-3">{{ item.icon }}</div>
          <h3 class="font-semibold text-gray-800">{{ item.name }}</h3>
          <p class="text-sm text-gray-500 mt-1">{{ item.desc }}</p>
        </div>
      </div>
    </div>

    <!-- 底部导航 -->
    <div class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-100 px-6 py-3 flex justify-around">
      <div class="text-orange-500 text-center">
        <div class="text-2xl">🏠</div>
        <p class="text-xs mt-1">首页</p>
      </div>
      <div @click="goTo('/elder/chat')" class="text-gray-400 text-center cursor-pointer">
        <div class="text-2xl">💬</div>
        <p class="text-xs mt-1">聊天</p>
      </div>
      <div @click="goTo('/elder/emergency')" class="text-gray-400 text-center cursor-pointer">
        <div class="text-2xl">🆘</div>
        <p class="text-xs mt-1">求助</p>
      </div>
      <div class="text-gray-400 text-center">
        <div class="text-2xl">👤</div>
        <p class="text-xs mt-1">我的</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

const features = [
  { name: '智能聊天', icon: '💬', desc: '陪您说说话', path: '/elder/chat' },
  { name: '用药提醒', icon: '💊', desc: '按时吃药', path: '/elder/medication' },
  { name: '紧急求助', icon: '🆘', desc: '一键呼救', path: '/elder/emergency' },
  { name: '视频通话', icon: '📹', desc: '见见家人', path: '/elder' },
]

function goTo(path: string) {
  router.push(path)
}
</script>