import api from './api'
import type { LoginCredentials } from '@/types/user'

export async function login(credentials: LoginCredentials) {
  const data = await api.post('/auth/login/', credentials)
  return data
}

export async function refresh(refresh_token: string) {
  const data = await api.post('/auth/refresh/', { refresh_token })
  return data
}

export async function registerFamily(data: any) {
  // Use the new RegisterApplication endpoint
  // data needs to be flattened as per RegisterApplicationSerializer
  // The frontend sends: { user: { username, password, real_name, phone }, patient_id_card, relationship }
  // We need to transform it to: { username, password, real_name, phone, patient_id_card, relationship }
  
  const payload = {
    username: data.user.username,
    password: data.user.password,
    real_name: data.user.real_name,
    phone: data.user.phone,
    patient_id_card: data.patient_id_card,
    relationship: data.relationship
  }
  
  return await api.post('/register-applications/', payload)
}
