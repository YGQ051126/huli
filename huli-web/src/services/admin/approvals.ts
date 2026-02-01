import api from '@/services/api'

export interface VisitApproval {
  id: number
  patient: number
  patient_name?: string // From serializer
  family_user: number
  family_name?: string // From serializer
  date: string
  time_slot: string
  notes?: string
  status: string
  created_at: string
  reviewer?: string
  reviewed_at?: string
  review_comment?: string
}

export interface LeaveApproval {
  id: number
  staff: number
  staff_name?: string
  leave_type: string
  start_date: string
  end_date: string
  days: number
  reason?: string
  status: string
  created_at: string
  department?: string
  reviewer?: string
  reviewed_at?: string
  review_comment?: string
}

export interface RegisterApplication {
  id: number
  username: string
  real_name: string
  phone: string
  patient_id_card: string
  relationship: string
  status: string
  created_at: string
  approved_by?: string
  approved_at?: string
  rejection_reason?: string
}

export interface ApprovalData {
  register_approvals: RegisterApplication[]
  visit_approvals: VisitApproval[]
  leave_approvals: LeaveApproval[]
}

export async function getApprovals(): Promise<ApprovalData> {
  const res = await api.get('/admin/approvals/')
  const data = res
  
  if (!data || typeof data !== 'object') {
    return {
      register_approvals: [],
      visit_approvals: [],
      leave_approvals: []
    }
  }
  
  return {
    register_approvals: Array.isArray((data as any).register_approvals) ? (data as any).register_approvals : [],
    visit_approvals: Array.isArray((data as any).visit_approvals) ? (data as any).visit_approvals : [],
    leave_approvals: Array.isArray((data as any).leave_approvals) ? (data as any).leave_approvals : []
  }
}

export async function approveRegisterApplication(id: number): Promise<void> {
  await api.post(`/register-applications/${id}/approve/`)
}

export async function rejectRegisterApplication(id: number, reason?: string): Promise<void> {
  await api.post(`/register-applications/${id}/reject/`, { reason })
}

export async function approveVisit(id: number): Promise<void> {
  await api.post(`/appointments/${id}/approve/`)
}

export async function rejectVisit(id: number, reason?: string): Promise<void> {
  await api.post(`/appointments/${id}/reject/`, { reason })
}

export async function approveLeave(id: number): Promise<void> {
  await api.post(`/admin/approvals/${id}/approve-leave/`)
}

export async function rejectLeave(id: number, reason?: string): Promise<void> {
  await api.post(`/admin/approvals/${id}/reject-leave/`, { reason })
}
