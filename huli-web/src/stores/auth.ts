import { defineStore } from 'pinia'
import { ref, computed, readonly } from 'vue'
import { useUserStore } from './user'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem('access_token'))
  const userStore = useUserStore()
  // 只有当token和user都存在时才认为已认证
  const isAuthenticated = computed(() => !!token.value && !!userStore.user)
  const user = computed(() => userStore.user)
  const setToken = (t: string | null) => {
    token.value = t
    if (t) localStorage.setItem('access_token', t)
    else localStorage.removeItem('access_token')
  }
  return {
    token: readonly(token),
    user,
    isAuthenticated,
    setToken
  }
})
