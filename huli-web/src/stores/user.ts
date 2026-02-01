import { defineStore } from 'pinia';
import { ref, computed, readonly } from 'vue';
import type { User, UserProfile, LoginCredentials } from '@/types/user'
import { useAuthStore } from './auth'
import { login as authLogin } from '@/services/auth'

export const useUserStore = defineStore('user', () => {
  // State
  const user = ref<User | null>(null);
  const profile = ref<UserProfile | null>(null);
  const loading = ref(false);
  const token = ref<string | null>(localStorage.getItem('access_token'));

  // 从localStorage恢复用户信息
  if (token.value) {
    try {
      const savedUserInfo = localStorage.getItem('user_info');
      if (savedUserInfo) {
        user.value = JSON.parse(savedUserInfo) as User;
      }
    } catch (error) {
      console.error('恢复用户信息失败:', error);
    }
  }

  // Getters
  const isLoggedIn = computed(() => !!user.value);
  const userRole = computed(() => user.value?.role);

  // Actions
  const login = async (credentials: LoginCredentials) => {
    loading.value = true;
    try {
      const normalizedInput = {
        username: String(credentials.username || '').trim().toLowerCase(),
        password: String(credentials.password || '')
      }
      const data: any = await authLogin(normalizedInput)
      const access = data?.access_token
      const refresh = data?.refresh_token
      const info = data?.user_info || data?.user
      const prof = data?.profile || null
      if (!access || !info) throw new Error('Login response incomplete')
      const normalized = { ...(info as any) }
      user.value = normalized as User
      profile.value = prof as UserProfile | null
      token.value = access
      localStorage.setItem('access_token', access)
      localStorage.setItem('user_info', JSON.stringify(normalized)) // 保存用户信息到localStorage
      if (refresh) localStorage.setItem('refresh_token', refresh)
      const auth = useAuthStore()
      auth.setToken(access)
    } catch (error: any) {
      const msg =
        (error?.response?.data?.message) ||
        (error?.message) ||
        'Login failed, please check network or credentials'
      throw new Error(String(msg))
    } finally {
      loading.value = false;
    }
  };

  const logout = () => {
    user.value = null;
    profile.value = null;
    token.value = null;
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    localStorage.removeItem('user_info') // 清除用户信息
    const auth = useAuthStore()
    auth.setToken(null)
  };

  const updateProfile = async (_data: Partial<UserProfile>) => {
    if (!profile.value) return;
    
    loading.value = true;
    try {
      // const updatedProfile = await userService.updateProfile(data);
      // profile.value = { ...profile.value, ...updatedProfile };
    } catch (error) {
      throw error;
    } finally {
      loading.value = false;
    }
  };

  return {
    user: readonly(user),
    profile: readonly(profile),
    loading: readonly(loading),
    token: readonly(token),
    isLoggedIn,
    userRole,
    login,
    logout,
    updateProfile
  };
});
