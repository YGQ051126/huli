import api from './api'

export interface ActivityGallery {
  id: string
  title: string
  description?: string
  activityDate: string
  mediaCount: number
  coverImage?: string
  createdAt: string
}

export interface ActivityMedia {
  id: string
  fileUrl: string
  filePath?: string
  fileType: 'image' | 'video'
  uploadTime: string
}

export interface CreateActivityData {
  title: string
  description?: string
  activityDate: string
  mediaFiles: File[]
  elderlyIds?: string[]
}

const rawBase = (import.meta as any)?.env?.VITE_API_BASE_URL || 'http://localhost:8000/api'
const mediaBase = rawBase.replace(/\/api\/?$/, '')

function toAbsoluteMediaUrl(fileUrl?: string, filePath?: string) {
  const url = fileUrl || ''
  if (url.startsWith('http://') || url.startsWith('https://')) return url
  
  // If we have a filePath but no valid url, construct from mediaBase
  if (filePath) {
    if (filePath.startsWith('http://') || filePath.startsWith('https://')) return filePath
    const cleanPath = filePath.startsWith('/') ? filePath.slice(1) : filePath
    return `${mediaBase}/media/${cleanPath}`
  }

  // If we only have url
  if (url.startsWith('/')) {
    // If it already contains /media/, assume it's family to root
    if (url.startsWith('/media/')) {
      return `${mediaBase}${url}`
    }
    // Otherwise it might be family to media root
    return `${mediaBase}/media${url}`
  }
  
  // Fallback
  return url ? `${mediaBase}/media/${url}` : ''
}

// Helper to adapt backend snake_case to frontend camelCase
function adaptActivity(data: any): ActivityGallery {
  return {
    id: data.id,
    title: data.title,
    description: data.description,
    activityDate: data.activity_date || data.activityDate,
    mediaCount: data.media_count || 0,
    coverImage: data.cover_image || data.coverImage,
    createdAt: data.created_at || data.createdAt
  }
}

function adaptMedia(data: any): ActivityMedia {
  const rawFileUrl = data.file_url || data.fileUrl || ''
  const rawFilePath = data.file_path || data.filePath || ''
  return {
    id: data.id,
    fileUrl: toAbsoluteMediaUrl(rawFileUrl, rawFilePath),
    filePath: rawFilePath || undefined,
    fileType: data.media_type || data.fileType || 'image',
    uploadTime: data.uploaded_at || data.uploadTime || new Date().toISOString()
  }
}

export async function getActivityGallery(startDate?: string, endDate?: string): Promise<ActivityGallery[]> {
  const res = await api.get('/activities/', {
    params: { start_date: startDate, end_date: endDate }
  })
  const results = (res as any).results || res // Handle DRF pagination or direct list
  return Array.isArray(results) ? results.map(adaptActivity) : []
}

export async function createActivity(data: CreateActivityData): Promise<ActivityGallery> {
  const formData = new FormData()
  formData.append('title', data.title)
  if (data.description) formData.append('description', data.description)
  formData.append('activity_date', data.activityDate)
  
  console.log('正在构建 FormData, 文件数量:', data.mediaFiles.length)
  data.mediaFiles.forEach((file, index) => {
    console.log(`添加文件 [${index}]:`, file.name, file.type, file.size)
    formData.append('media_files', file)
  })
  
  if (data.elderlyIds) {
    data.elderlyIds.forEach((id) => {
      formData.append('elderly_ids', id)
    })
  }
  
  // Debug FormData
  // for (const pair of formData.entries()) {
  //   console.log('FormData Entry:', pair[0], pair[1]);
  // }
  
  const res = await api.post('/activities/', formData)
  return adaptActivity(res)
}

export async function getActivityDetail(id: string): Promise<ActivityGallery> {
  const res = await api.get(`/activities/${id}/`)
  return adaptActivity(res)
}

export async function getActivityMedia(activityId: string): Promise<ActivityMedia[]> {
  const res = await api.get('/media/', {
    params: { activity: activityId }
  })
  const results = (res as any).results || res
  return Array.isArray(results) ? results.map(adaptMedia) : []
}
