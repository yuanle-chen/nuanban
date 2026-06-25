<template>
  <router-view />
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useUserStore } from './stores/user'
import { getCurrentUser } from './api/auth'

const userStore = useUserStore()

onMounted(async () => {
  if (userStore.token && !userStore.userInfo) {
    try {
      const res: any = await getCurrentUser()
      userStore.setUserInfo(res)
    } catch (error) {
      console.log('获取用户信息失败')
    }
  }
})
</script>
