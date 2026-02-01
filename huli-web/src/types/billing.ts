import type { BillStatus, PaymentStatus } from './common'

export interface BillItem {
  id: string
  billId: string
  itemName: string
  quantity: number
  unitPrice: number
  amount: number
}

export interface Bill {
  id: string
  patientId: string
  month: string
  totalAmount: number
  paidAmount: number
  status: BillStatus
  items: BillItem[]
  createdAt: string
  updatedAt: string
}

export interface Payment {
  id: string
  billId: string
  amount: number
  method: 'alipay' | 'wechat' | 'bank'
  status: PaymentStatus
  transactionId: string
  paidAt: string
  createdAt: string
}
