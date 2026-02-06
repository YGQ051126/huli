import api from './api'

export interface Message {
  id: number
  sender: number
  sender_name?: string
  sender_avatar?: string
  receiver: number
  receiver_name?: string
  type: 'text' | 'voice' | 'image' | 'system'
  content: string
  status: 'sent' | 'delivered' | 'read'
  is_read: boolean
  created_at: string
  patient?: number
  duration?: number
  file_url?: string
}

export interface CreateMessageData {
  receiver: number
  content: string
  type?: 'text' | 'voice' | 'image'
  patient?: number
  duration?: number
  file_url?: string
}

export async function getMessages(params?: any): Promise<Message[]> {
  const data: any = await api.get('/messages/', { params })
  if (Array.isArray(data)) return data as Message[]
  if (data && typeof data === 'object' && Array.isArray((data as any).results)) {
    return (data as any).results as Message[]
  }
  return []
}

export async function sendMessage(data: CreateMessageData): Promise<Message> {
  const result: any = await api.post('/messages/', data)
  return result as Message
}

export async function markMessageRead(id: number): Promise<void> {
  await api.post(`/messages/${id}/read/`)
}

// Aliases for compatibility
export const getStaffMessages = (receiverId?: string | number) => getMessages({ receiver: receiverId })
export const sendStaffMessage = sendMessage
