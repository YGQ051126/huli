import api from './api'

export interface ApprovalRequest {
  id: string
  approvalType: 'visit' | 'leave'
  applicantId: string
  applicantName: string
  elderlyId?: string
  elderlyName?: string
  appointmentDate?: string
  appointmentTime?: string
  leaveType?: string
  startDate?: string
  endDate?: string
  reason: string
  status: 'pending' | 'approved' | 'rejected'
  approvedBy?: string
  approvedAt?: string
  remark?: string
  createdAt: string
}

export interface ApproveRequestData {
  action: 'approve' | 'reject'
  remark?: string
}

export async function getApprovals(approvalType?: string, status?: string): Promise<ApprovalRequest[]> {
  const res = await api.get('/api/v1/admin/approvals', {
    params: { approval_type: approvalType, status }
  })
  return res.data.results || res.data
}

export async function approveRequest(approvalId: string, data: ApproveRequestData): Promise<void> {
  await api.post(`/admin/approvals/${approvalId}/approve`, data)
}

