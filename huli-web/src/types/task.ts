export interface CareTask {
  id: string
  patientId: string
  staffId: string
  taskType: string
  description: string
  scheduledTime: string
  status: 'pending' | 'in_progress' | 'completed' | 'delayed' | 'cancelled'
  priority: 'low' | 'medium' | 'high'
  notes?: string
  createdAt: string
  updatedAt: string
}
