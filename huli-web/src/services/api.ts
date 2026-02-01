import axios, { type AxiosInstance, type AxiosResponse, type AxiosError } from 'axios'
import { ElMessage } from 'element-plus'

const rawBase = (import.meta as any)?.env?.VITE_API_BASE_URL || 'http://localhost:8000/api'
const baseURL = rawBase.replace(/\/$/, '') + (rawBase.endsWith('/api') ? '/v1' : '/api/v1')

console.log('API Configuration:')
console.log('rawBase:', rawBase)
console.log('baseURL:', baseURL)
console.log('VITE_API_BASE_URL:', (import.meta as any)?.env?.VITE_API_BASE_URL)

const api: AxiosInstance = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

let isRefreshing = false
let pendingQueue: Array<() => void> = []

api.interceptors.request.use(
  config => {
    // 排除不需要认证的接口
    const publicUrls = [
      '/auth/login/',
      '/auth/register/family/',
      '/auth/register/staff/',
      '/register-applications/'
    ]
    const isPublic = publicUrls.some(url => {
      // 特殊例外：如果是 register-applications 且包含 approve 或 reject，则不是 public，需要认证
      if (url === '/register-applications/' && config.url && (config.url.includes('/approve/') || config.url.includes('/reject/'))) {
        return false
      }
      return config.url?.includes(url)
    })
    
    const token = localStorage.getItem('access_token')
    if (token && !isPublic) {
      const headers: Record<string, string> = (config.headers as any) || {}
      headers.Authorization = `Bearer ${token}`
      config.headers = headers as any
    }
    
    try {
      const method = (config.method || 'get').toUpperCase()
      const url = config.url || ''
      const fullUrl = `${String(config.baseURL || '')}${url}`
      console.groupCollapsed('[api] request')
      console.log('method:', method)
      console.log('url:', url)
      console.log('baseURL:', config.baseURL)
      console.log('fullUrl:', fullUrl)
      console.log('params:', (config as any).params)
      console.log('data:', config.data)
      console.groupEnd()
    } catch (e) {
      console.error('[api] request log failed:', e)
    }

    // 如果数据是 FormData，删除 Content-Type 头，让浏览器自动设置（包含 boundary）
    if (config.data instanceof FormData) {
      // 需要类型断言，因为 headers 类型定义可能不包含 delete
      const headers = config.headers as any
      delete headers['Content-Type']
    }
    
    return config
  },
  error => Promise.reject(error)
)

api.interceptors.response.use(
  (response: AxiosResponse) => {
    const data: any = response.data
    try {
      console.groupCollapsed('[api] response')
      console.log('status:', response.status)
      console.log('url:', response.config?.url)
      console.log('data:', data)
      console.groupEnd()
    } catch (e) {
      console.error('[api] response log failed:', e)
    }
    if (data && typeof data === 'object' && 'code' in data && 'data' in data) {
      if (data.code === 200 || data.code === 201) return data.data
      const msg = String(data.message || 'Request Failed')
      ElMessage.error(msg)
      return Promise.reject(new Error(msg))
    }
    return data
  },
  async (error: AxiosError) => {
    try {
      console.groupCollapsed('[api] error')
      console.log('message:', error.message)
      console.log('code:', (error as any).code)
      console.log('url:', error.config?.url)
      console.log('method:', error.config?.method)
      console.log('params:', (error.config as any)?.params)
      console.log('data:', error.config?.data)
      console.log('status:', error.response?.status)
      console.log('responseData:', error.response?.data)
      console.groupEnd()
    } catch (e) {
      console.error('[api] error log failed:', e)
    }
    if (error.response && error.response.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token')
      if (!refreshToken) {
        ElMessage.error('请先登录后再操作')
        return Promise.reject(error)
      }
      const retryOriginal = () => {
        const cfg = error.config!
        return api(cfg)
      }
      if (isRefreshing) {
        await new Promise<void>(resolve => pendingQueue.push(resolve))
        return retryOriginal()
      }
      isRefreshing = true
      try {
        const refreshClient = axios.create({ baseURL })
        const resp = await refreshClient.post('/token/refresh/', { refresh: refreshToken })
        const payload: any = resp.data && resp.data.data ? resp.data.data : resp.data
        const newAccess = payload?.access || payload?.access_token
        const newRefresh = payload?.refresh_token || refreshToken
        if (newAccess) {
          localStorage.setItem('access_token', newAccess)
          localStorage.setItem('refresh_token', newRefresh)
          pendingQueue.forEach(fn => fn())
          pendingQueue = []
          return retryOriginal()
        }
        throw new Error('Refresh token failed')
      } catch (e) {
        pendingQueue = []
        ElMessage.error('登录已过期，请重新登录')
        return Promise.reject(e)
      } finally {
        isRefreshing = false
      }
    }
    let message = 'Unknown Error'
    if (error.response) {
      const status = error.response.status
      switch (status) {
        case 400:
          message = '请求参数错误'
          break
        case 403:
          message = '没有权限访问该资源'
          break
        case 404:
          message = '请求的资源不存在'
          break
        case 500:
          message = '服务器内部错误'
          break
        default:
          message = `请求失败: ${status}`
      }
    } else if (error.request) {
      message = '网络错误：未收到响应'
      console.error('Network Error Details:', error.toJSON ? error.toJSON() : error)
    } else {
      message = String(error.message || error)
      console.error('Request Setup Error:', error)
    }
    ElMessage.error(message)
    return Promise.reject(new Error(message))
  }
)

export default api
