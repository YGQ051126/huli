import type { AppointmentStatus } from './common'

export interface Appointment {
  id: string
  type: 'visit' | 'service' | 'consultation'
  patientId: string
  familyId?: string
  staffId?: string
  date: string
  timeSlot: string
  status: AppointmentStatus
  notes?: string
  createdAt: string
  updatedAt: string
}

export interface CreateAppointmentData {
  type: 'visit' | 'service' | 'consultation'
  patientId: string
  familyId?: string
  staffId?: string
  date: string
  timeSlot: string
  notes?: string
}

export interface AppointmentFilters {
  type?: 'visit' | 'service' | 'consultation'
  patientId?: string
  status?: AppointmentStatus
}
