 

export interface Patient {
  id: string
  name: string
  age: number
  gender: 'male' | 'female'
  avatar?: string
  idCard: string
  phone?: string
  address?: string
  health_level: string
  care_level: string
  room?: {
    id: string
    room_number: string
    bed1_id: string
    bed2_id: string
    bed3_id: string
    bed4_id: string
  }
  bed_id: string
  admission_date: string
  status: 'active' | 'discharged' | 'transferred'
  created_at: string
  updated_at: string
}

export interface VitalSigns {
  temperature: number
  heartRate: number
  bloodPressure: {
    systolic: number
    diastolic: number
  }
  respiratoryRate: number
  oxygenSaturation: number
}

export interface HealthRecord {
  id: string
  patientId: string
  recordDate: string
  vitalSigns: VitalSigns
  diet: string
  sleep: string
  bowelMovement: string
  mentalState: string
  notes?: string
  recordedBy: string
  createdAt: string
}
