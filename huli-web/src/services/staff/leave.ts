import api from '@/services/api'

export interface LeaveRequest {
  id: number
  staff?: number
  staff_name?: string
  leave_type?: string // 'sick' | 'personal' | 'annual' | 'emergency'
  type: string // API field name is 'type'
  start_date: string
  end_date: string
  reason: string
  status: string // 'pending' | 'approved' | 'rejected' | 'cancelled'
  created_at: string
  rejection_reason?: string 
}

export interface CreateLeaveRequestParams {
  type: string
  start_date: string
  end_date: string
  reason: string
}

export const getLeaveRequests = () => {
  // Use the full URL if necessary or check how other services are doing it
  // In users/urls.py: router.register(r'leave-requests', ...)
  // This means the URL is /api/v1/leave-requests/ NOT /api/v1/users/leave-requests/
  // because router is included at path('api/v1/', include('users.urls'))
  // AND users/urls.py has path('', include(router.urls))
  // BUT the router prefix is empty for the include in users/urls.py?
  // Let's check care_platform/urls.py
  return api.get<LeaveRequest[]>('/leave-requests/')
}

export const createLeaveRequest = (data: CreateLeaveRequestParams) => {
  return api.post<LeaveRequest>('/leave-requests/', data)
}

// Optional: Cancel request
export const cancelLeaveRequest = (id: number) => {
    return api.delete(`/leave-requests/${id}/`)
}
