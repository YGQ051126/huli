import api from './api'

export interface CareReminder {
  id: string
  elderlyId: string
  elderlyName: string
  reminderType: 'birthday' | 'festival'
  title: string
  content: string
  reminderDate: string
  isParticipated: boolean
  participationType?: 'gift' | 'visit' | 'message'
  createdAt: string
}

export interface ParticipateReminderData {
  participationType: 'gift' | 'visit' | 'message'
  message?: string
}

export async function getCareReminders(elderlyId: string, reminderType?: string): Promise<CareReminder[]> {
  const res = await api.get('/family/care-reminders', {
    params: { elderlyId, reminder_type: reminderType }
  })
  return res.data.results || res.data
}

export async function participateReminder(reminderId: string, data: ParticipateReminderData): Promise<void> {
  await api.post(`/family/care-reminders/${reminderId}/participate`, data)
}

