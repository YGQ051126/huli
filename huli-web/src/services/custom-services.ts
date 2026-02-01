import api from './api'

export interface CustomService {
  id: string
  elderlyId: string
  serviceType: string
  serviceName: string
  description?: string
  expectedDate: string
  amount: number
  status: 'pending' | 'approved' | 'completed' | 'cancelled'
  feedback?: string
  rating?: number
  createdAt: string
  updatedAt: string
}

export interface CreateCustomServiceData {
  elderlyId: string
  serviceType: string
  serviceName: string
  description?: string
  expectedDate: string
  amount: number
}

export interface ServiceFeedback {
  rating: number
  feedback?: string
}

export async function getCustomServices(elderlyId: string, status?: string): Promise<CustomService[]> {
  const res = await api.get('/family/custom-services', {
    params: { elderlyId, status }
  })
  return res.data.results || res.data
}

export async function createCustomService(data: CreateCustomServiceData): Promise<CustomService> {
  const res = await api.post('/family/custom-services', data)
  return res.data
}

export async function submitServiceFeedback(serviceId: string, feedback: ServiceFeedback): Promise<void> {
  await api.post(`/family/custom-services/${serviceId}/feedback`, feedback)
}

