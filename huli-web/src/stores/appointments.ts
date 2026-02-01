import { defineStore } from 'pinia'
import { ref, computed, readonly } from 'vue'
import type { Appointment, CreateAppointmentData, AppointmentFilters } from '@/types/appointment'
import { getAppointments, createAppointment, cancelAppointment } from '@/services/appointments'

export const useAppointmentStore = defineStore('appointments', () => {
  const appointments = ref<Appointment[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  const upcomingAppointments = computed(() =>
    appointments.value.filter(apt => apt.status !== 'cancelled')
  )

  const pastAppointments = computed(() =>
    appointments.value.filter(apt => apt.status === 'completed' || apt.status === 'cancelled')
  )

  const fetchAppointments = async (filters?: AppointmentFilters) => {
    loading.value = true
    error.value = null
    try {
      const list = await getAppointments(filters)
      appointments.value = list
    } catch (err) {
      error.value = err instanceof Error ? err.message : '获取预约失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const createApt = async (data: CreateAppointmentData) => {
    loading.value = true
    error.value = null
    try {
      const apt = await createAppointment(data)
      appointments.value.push(apt)
      return apt
    } catch (err) {
      error.value = err instanceof Error ? err.message : '创建预约失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  const cancelApt = async (id: string) => {
    loading.value = true
    error.value = null
    try {
      await cancelAppointment(id)
      const item = appointments.value.find(a => a.id === id)
      if (item) item.status = 'cancelled'
    } catch (err) {
      error.value = err instanceof Error ? err.message : '取消预约失败'
      throw err
    } finally {
      loading.value = false
    }
  }

  return {
    appointments: readonly(appointments),
    loading: readonly(loading),
    error: readonly(error),
    upcomingAppointments,
    pastAppointments,
    fetchAppointments,
    createApt,
    cancelApt
  }
})
