import api from './api'
import type { CareRecordTemplate, CareRecordPayload } from '@/types/care'

export async function getCareRecordTemplate(patientId: string): Promise<CareRecordTemplate> {
  const res = await api.get('/staff/care-records/template', { params: { patient_id: patientId } })
  return res.data
}

export async function saveCareRecord(data: CareRecordPayload): Promise<void> {
  await api.post('/staff/care-records', data)
}

export async function submitCareRecord(data: CareRecordPayload): Promise<void> {
  await api.post('/staff/care-records/submit', data)
}

export async function getCareRecords(patientId: string): Promise<any[]> {
  const res: any = await api.get(`/patients/${patientId}/care-records/`)
  if (Array.isArray(res)) return res
  if (res && typeof res === 'object' && Array.isArray(res.results)) {
    return res.results
  }
  return []
}

export async function getDailyCareTasks(patientId: string): Promise<any[]> {
  const res: any = await api.get('/daily-care-tasks/', { params: { patient: patientId } })
  if (Array.isArray(res)) return res
  if (res && typeof res === 'object' && Array.isArray(res.results)) {
    return res.results
  }
  return []
}


