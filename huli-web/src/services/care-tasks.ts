import api from './api'

export interface DailyCareTask {
  id: number
  patient: number
  patient_name: string
  patient_room: string
  patient_care_level: string
  task_date: string
  vital_signs_normal: boolean
  diet_normal: boolean
  mental_normal: boolean
  is_completed: boolean
  updated_at: string
}

export const getDailyCareTasks = () => {
  return api.get<DailyCareTask[]>('/daily-care-tasks/today/')
}

export const pullLatestTasks = () => {
  return api.get<DailyCareTask[]>('/daily-care-tasks/pull_latest/')
}

export const batchUpdateTasks = (tasks: Partial<DailyCareTask>[]) => {
  return api.post('/daily-care-tasks/batch_update/', { tasks })
}
