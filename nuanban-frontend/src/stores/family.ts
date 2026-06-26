import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMyElders } from '../api/family'

export const useFamilyStore = defineStore('family', () => {
  const elders = ref<any[]>([])
  const currentElder = ref<any>(null)

  async function fetchElders() {
    try {
      const res: any = await getMyElders()
      elders.value = res
      if (res.length > 0 && !currentElder.value) {
        currentElder.value = res[0]
      }
      return res
    } catch (error) {
      console.error('获取老人列表失败', error)
      throw error
    }
  }

  function setCurrentElder(elder: any) {
    currentElder.value = elder
  }

  function $reset() {
    elders.value = []
    currentElder.value = null
  }

  return { elders, currentElder, fetchElders, setCurrentElder, $reset }
})