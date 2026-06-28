import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMyElders, getMyChildren } from '../api/family'

export const useFamilyStore = defineStore('family', () => {
  const elders = ref<any[]>([])
  const children = ref<any[]>([])
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

  async function fetchChildren() {
    try {
      const res: any = await getMyChildren()
      children.value = res
      return res
    } catch (error) {
      console.error('获取子女列表失败', error)
      throw error
    }
  }

  function setCurrentElder(elder: any) {
    currentElder.value = elder
  }

  function $reset() {
    elders.value = []
    children.value = []
    currentElder.value = null
  }

  return { elders, children, currentElder, fetchElders, fetchChildren, setCurrentElder, $reset }
})