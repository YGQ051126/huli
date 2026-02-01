import api from '@/services/api'

export interface Bill {
  id: number
  patient: number
  family: number
  bill_type: string
  month: string
  total_amount: number
  paid_amount: number
  status: string // 'unpaid' | 'paid' | 'partially_paid'
  due_date: string
  created_at: string
}

export interface PaymentResponse {
  order_id: string
  cashier_url: string
  total_amount: number
}

export const getBills = async (): Promise<Bill[]> => {
  return (await api.get('/family/bills/')) as unknown as Bill[]
}

export const refreshBills = async (): Promise<{ created: number, month: string }> => {
  return (await api.post('/refresh-bills/')) as unknown as { created: number, month: string }
}

export const createPayment = async (billIds: number[]): Promise<PaymentResponse> => {
  return (await api.post('/bulk-payments/create/', { bill_ids: billIds })) as unknown as PaymentResponse
}
