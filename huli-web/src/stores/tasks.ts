import { defineStore } from 'pinia'
import { ref, readonly } from 'vue'
import { getTasks, completeTask, delayTask, type BackendTask } from '@/services/tasks'

export const useTasksStore = defineStore('tasks', () => {
  const list = ref<BackendTask[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchTasks = async () => {
    loading.value = true
    error.value = null
    try {
      list.value = await getTasks()
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取任务失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const finish = async (id: string) => {
    loading.value = true
    error.value = null
    try {
      await completeTask(id)
      const item = list.value.find(t => t.id === id)
      if (item) item.status = 'completed'
    } catch (err) {
      error.value = err instanceof Error ? err.message : '完成任务失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const delay = async (id: string, reason: string) => {
    loading.value = true
    error.value = null
    try {
      await delayTask(id, reason)
      const item = list.value.find(t => t.id === id)
      if (item) item.status = 'delayed'
    } catch (err) {
      error.value = err instanceof Error ? err.message : '延迟任务失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    list: readonly(list),
    loading: readonly(loading),
    error: readonly(error),
    fetchTasks,
    finish,
    delay
  }
})
