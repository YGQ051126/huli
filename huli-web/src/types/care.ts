import type { VitalSigns } from './patient'

export interface CareRecordFieldOption {
  label: string
  value: string | number | boolean
}

export type CareRecordFieldType = 'text' | 'textarea' | 'select' | 'number' | 'switch' | 'checkbox_group'

export interface CareRecordField {
  id: string
  label: string
  type: CareRecordFieldType
  placeholder?: string
  required?: boolean
  options?: CareRecordFieldOption[]
}

export interface CareRecordTemplate {
  id: string
  name: string
  description?: string
  fields: CareRecordField[]
}

export interface CareRecordPayload {
  patientId: string
  staffId: string
  recordDate: string
  templateId: string
  status: 'draft' | 'submitted'
  vitalSigns?: VitalSigns
  fields: Record<string, string | number | boolean>
}

export interface CareRecordHistoryItem {
  id: string
  recordDate: string
  staffName: string
  status: 'draft' | 'submitted' | 'approved'
}


