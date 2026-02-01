import api from './api'
import type { Appointment, CreateAppointmentData, AppointmentFilters } from '@/types/appointment'

export async function getAppointments(filters?: AppointmentFilters): Promise<Appointment[]> {
  const res = await api.get('/family/appointments/', { params: filters })
  // Handle paginated response from DRF
  if (res && typeof res === 'object' && 'results' in res && Array.isArray((res as any).results)) {
    return (res as any).results
  }
  // Handle standard array response (if pagination is disabled or different wrapper)
  return Array.isArray(res) ? res : []
}

export async function createAppointment(data: CreateAppointmentData): Promise<Appointment> {
  const res = await api.post('/family/appointments/', data)
  return res as unknown as Appointment
}

export async function cancelAppointment(id: string): Promise<void> {
  await api.post(`/family/appointments/${id}/cancel/`)
}
