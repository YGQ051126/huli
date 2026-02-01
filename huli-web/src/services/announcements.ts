import api from './api'
import type { Announcement, AnnouncementQueryParams } from '@/types/announcement'

export async function getAnnouncements(params?: AnnouncementQueryParams): Promise<Announcement[]> {
  console.log('调用公告API，参数:', params)
  try {
    const res = await api.get('/announcements/', { params })
    console.log('公告API原始响应:', res)
    
    // 检查响应数据结构
    if (!res) {
      console.error('API响应为空')
      return []
    }
    
    // 如果res本身就是数组，直接返回
    if (Array.isArray(res)) {
      console.log('响应是数组，直接返回:', res.length, '条公告')
      return res
    }
    
    // Django REST Framework格式: {count: number, results: Announcement[]}
    if ('results' in res && Array.isArray(res.results)) {
      console.log('Django REST Framework格式，返回results:', res.results.length, '条公告')
      return res.results as Announcement[]
    }
    
    // 标准格式: {code: number, data: Announcement[]}
    if ('data' in res && Array.isArray(res.data)) {
      console.log('标准响应格式，返回data:', res.data.length, '条公告')
      return res.data as Announcement[]
    }
    
    console.error('无法识别的响应格式，返回空数组。res结构:', Object.keys(res))
    return []
    
  } catch (error) {
    console.error('获取公告API调用失败:', error)
    throw error
  }
}

export async function getAnnouncementById(id: string | number): Promise<Announcement> {
  try {
    const res = await api.get(`/announcements/${id}/`)
    console.log('获取公告详情API响应:', res)
    
    // 处理不同的响应格式
    if (!res) {
      throw new Error('API响应为空')
    }
    
    // 如果res本身就是公告对象
    if ('id' in res && 'title' in res) {
      return res as unknown as Announcement
    }
    
    console.error('无法识别的公告详情响应格式:', res)
    throw new Error('无法识别的API响应格式')
  } catch (error) {
    console.error('获取公告详情失败:', error)
    throw error
  }
}

export async function markAllAnnouncementsRead(): Promise<void> {
  // 批量标记已读功能暂未实现
  throw new Error('批量标记已读功能暂未实现')
}