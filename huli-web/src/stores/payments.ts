import { defineStore } from 'pinia'
import { ref, readonly } from 'vue'
import type { Bill } from '@/types/billing'
import { getBills, payBill } from '@/services/payments'

export const usePaymentsStore = defineStore('payments', () => {
  const bills = ref<Bill[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const fetchBills = async (patientId?: string) => {
    loading.value = true
    error.value = null
    try {
      bills.value = await getBills(patientId)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'èŽ·å�–è´¦å�•å¤±è´¥'
      throw err
    } finally {
      loading.value = false
    }
  }

  const pay = async (billId: string, amount: number, method: 'alipay' | 'wechat' | 'bank' | 'balance') => {
    loading.value = true
    error.value = null
    try {
      await payBill(billId, amount, method)
      // Refresh bills list to get updated status and amounts from backend
      // Or manually update if backend response is not used for full refresh
      const bill = bills.value.find(b => b.id === billId)
      if (bill) {
        // Note: property names might be snake_case from backend or camelCase from type definition
        // Let's assume we need to update local state or re-fetch
        // Re-fetching is safer
        await fetchBills() 
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'Ö§¸¶Ê§°Ü'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    bills: readonly(bills),
    loading: readonly(loading),
    error: readonly(error),
    fetchBills,
    pay
  }
})
