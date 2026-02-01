import { defineStore } from 'pinia'
import { ref, readonly } from 'vue'
import type { Patient } from '@/types/patient'
import { getPatients } from '@/services/patients'

export const usePatientsStore = defineStore('patients', () => {
  const list = ref<Patient[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchPatients = async () => {
    loading.value = true
    error.value = null
    try {
      list.value = await getPatients()
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取患者列表失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    list: readonly(list),
    loading: readonly(loading),
    error: readonly(error),
    fetchPatients
  }
})
