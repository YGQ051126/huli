import api from '@/services/api'

export type ReportQuery = {
  type: 'daily' | 'weekly' | 'monthly'
  startDate?: string
  endDate?: string
}

export async function getReports(query: ReportQuery): Promise<any> {
  const res = await api.get('/admin/reports/', { params: query })
  return res
}

