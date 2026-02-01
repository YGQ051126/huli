import api from './api'
import type { Bill, Payment } from '@/types/billing'

export async function getBills(patientId?: string): Promise<Bill[]> {
  const res = await api.get('/family/bills/', { params: { patientId } })
  return Array.isArray(res) ? res : []
}

export async function payBill(billId: string, amount: number, method: 'alipay' | 'wechat' | 'bank' | 'balance'): Promise<Payment> {
  const res = await api.post(`/family/bills/${billId}/pay/`, { amount, payment_method: method })
  return res as unknown as Payment
}
