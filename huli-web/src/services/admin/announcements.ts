import api from '@/services/api'

export interface Announcement {
  id: number
  title: string
  content: string
  target_role: 'all' | 'family' | 'staff'
  status: 'published' | 'draft' | 'retracted'
  publish_time: string
  expire_time?: string
  created_by?: {
    id: number
    real_name: string
  }
}

export interface AnnouncementCreateData {
  title: string
  content: string
  target_role: string
  expire_time?: string
  status?: string
}

export async function getAnnouncements(): Promise<Announcement[]> {
  const res = await api.get('/announcements/')
  console.log('后端原始响应:', res)
  
  // 处理 DRF 分页格式
  const data = (res as any)
  if (data && typeof data === 'object') {
    if (Array.isArray(data.results)) {
      return data.results
    }
    if (Array.isArray(data.data)) {
      return data.data
    }
    if (Array.isArray(data)) {
      return data
    }
  }
  
  return []
}

export async function createAnnouncement(data: AnnouncementCreateData): Promise<Announcement> {
  const res = await api.post('/announcements/', data)
  return res.data
}

export async function updateAnnouncement(id: number, data: Partial<AnnouncementCreateData>): Promise<Announcement> {
  const res = await api.patch(`/announcements/${id}/`, data)
  return res.data
}

export async function deleteAnnouncement(id: number): Promise<void> {
  await api.delete(`/announcements/${id}/`)
}

export async function retractAnnouncement(id: number): Promise<void> {
  await api.patch(`/announcements/${id}/`, { status: 'retracted' })
}
