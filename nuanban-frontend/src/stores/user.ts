import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useUserStore = defineStore('user', () => {
  const token = ref<string | null>(localStorage.getItem('token'))
  const userInfo = ref<any>(null)
  const role = ref<string | null>(localStorage.getItem('role'))

  function setToken(newToken: string, userRole: string) {
    token.value = newToken
    role.value = userRole
    localStorage.setItem('token', newToken)
    localStorage.setItem('role', userRole)
  }

  function setUserInfo(info: any) {
    userInfo.value = info
  }

  function logout() {
    token.value = null
    userInfo.value = null
    role.value = null
    localStorage.removeItem('token')
    localStorage.removeItem('role')
  }

  return { token, userInfo, role, setToken, setUserInfo, logout }
})