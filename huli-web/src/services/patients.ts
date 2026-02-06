import api from './api'
import type { Patient } from '@/types/patient'
import { useUserStore } from '@/stores/user'

export async function getPatients(): Promise<Patient[]> {
  const store = useUserStore()
  const role = store.userRole
  const path = role === 'admin' || role === 'staff' ? '/admin/elderly/' : '/family/elderly/'
  const res = await api.get(path)
  
  // Handle paginated response
  if (res && typeof res === 'object' && 'results' in (res as any)) {
    return (res as any).results as unknown as Patient[]
  }
  
  return Array.isArray(res) ? res as unknown as Patient[] : []
}

export async function createPatient(patientData: Omit<Patient, 'id' | 'created_at' | 'updated_at'>): Promise<Patient> {
  const store = useUserStore()
  const role = store.userRole
  const path = role === 'admin' || role === 'staff' ? '/admin/elderly/' : '/family/elderly/'
  const res = await api.post(path, patientData)
  return res as unknown as Patient
}

export async function updatePatient(id: string, patientData: Partial<Patient>): Promise<Patient> {
  const store = useUserStore()
  const role = store.userRole
  const path = role === 'admin' || role === 'staff' ? '/admin/elderly/' : '/family/elderly/'
  const res = await api.put(`${path}${id}/`, patientData)
  return res as unknown as Patient
}

export async function deletePatient(id: string): Promise<void> {
  const store = useUserStore()
  const role = store.userRole
  const path = role === 'admin' || role === 'staff' ? '/admin/elderly/' : '/family/elderly/'
  await api.delete(`${path}${id}/`)
}

export async function getRooms(): Promise<any[]> {
  try {
    console.log('开始调用getRooms API...')
    const res = await api.get('/rooms/')
    console.log('getRooms response:', res)
    
    // 处理分页格式 { count: 9, next: null, previous: null, results: [...] }
    if (res && typeof res === 'object') {
      if (Array.isArray((res as any).results)) {
        console.log('Found paginated results:', (res as any).results)
        return (res as any).results
      }
      if (Array.isArray((res as any).data)) {
        console.log('Found data array:', (res as any).data)
        return (res as any).data
      }
    }
    
    // 如果不是分页格式，直接返回
    if (Array.isArray(res)) {
      console.log('Returning array directly:', res)
      return res
    }
    
    console.log('Returning empty array - no valid data found')
    return []
  } catch (error) {
    console.error('getRooms API调用失败:', error)
    console.error('错误类型:', error?.constructor?.name)
    console.error('错误消息:', (error as any)?.message)
    console.error('错误响应:', (error as any)?.response?.data)
    console.error('错误状态码:', (error as any)?.response?.status)
    console.error('请求URL:', (error as any)?.config?.url)
    console.error('请求方法:', (error as any)?.config?.method)
    throw error
  }
}

export async function getRoomAvailableBeds(roomId: string): Promise<any> {
  const res = await api.get(`/api/v1/rooms/${roomId}/available_beds/`)
  // API interceptor returns data.data
  return res
}

export async function getFamilyDashboard(): Promise<any> {
  const res = await api.get('/patients/family/dashboard/')
  return res.data || res
}