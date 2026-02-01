export interface Message {
  id: string
  senderId: string
  receiverId: string
  type: 'text' | 'voice' | 'image' | 'system'
  content: string
  duration?: number
  status: 'sent' | 'delivered' | 'read'
  created_at: string
}

export interface Notification {
  id: string
  userId: string
  title: string
  content: string
  type: 'system' | 'service' | 'health' | 'payment'
  status: 'unread' | 'read'
  created_at: string
}
