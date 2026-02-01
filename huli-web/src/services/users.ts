import api from './api'
import type { User } from '@/types/user'

export interface UserQueryParams {
  role?: 'admin' | 'staff' | 'family'
  status?: 'active' | 'inactive' | 'pending'
  search?: string
  page?: number
  page_size?: number
}

export async function getUsers(params?: UserQueryParams): Promise<User[]> {
  try {
    console.log('getUsers called with params:', params)
    const data: any = await api.get('/users/', { params })
    console.log('getUsers response data:', data)
    
    // Handle pagination format
    if (Array.isArray(data)) {
      console.log('Returning array data:', data)
      return data as User[]
    }
    if (data && typeof data === 'object') {
      if (Array.isArray(data.results)) {
        console.log('Returning paginated results:', data.results)
        return data.results as User[]
      }
      if (Array.isArray(data.data)) {
        console.log('Returning data array:', data.data)
        return data.data as User[]
      }
    }
    
    console.log('No valid data format found, returning empty array. Data:', data)
    return []
  } catch (error: any) {
    console.error('Error in getUsers:', error)
    console.error('Error details:', error?.response?.data)
    console.error('Error status:', error?.response?.status)
    console.error('Error message:', error?.message)
    return []
  }
}

export async function getUserById(id: string | number): Promise<User> {
  const data: any = await api.get(`/users/${id}/`)
  return data as User
}

export async function createUser(userData: Partial<User>): Promise<User> {
  const data: any = await api.post('/users/', userData)
  return data as User
}

export async function updateUser(id: string | number, userData: Partial<User>): Promise<User> {
  const data: any = await api.put(`/users/${id}/`, userData)
  return data as User
}

export async function deleteUser(id: string | number): Promise<void> {
  await api.delete(`/users/${id}/`)
}

// Family specific functions
// 直接调用family-users API来获取家属用户
// 然后从返回的家属用户中提取User信息
export async function getFamilyUsers(params?: Omit<UserQueryParams, 'role'>): Promise<User[]> {
  try {
    console.log('=== getFamilyUsers 开始调用 ===')
    console.log('getFamilyUsers called with params:', params)
    console.log('API baseURL:', (api as any).defaults?.baseURL)
    console.log('Current token:', localStorage.getItem('access_token'))
    
    // 直接调用family-users API
    console.log('Calling /family-users/ API...')
    const familyUsersData: any = await api.get('/family-users/', { params })
    console.log('family-users API response data:', familyUsersData)
    
    let familyUserObjects: any[] = []
    
    // 处理不同的数据格式
    if (Array.isArray(familyUsersData)) {
      familyUserObjects = familyUsersData
      console.log('Using array data directly, count:', familyUserObjects.length)
    } else if (familyUsersData && typeof familyUsersData === 'object') {
      if (Array.isArray(familyUsersData.results)) {
        familyUserObjects = familyUsersData.results
        console.log('Using paginated results, count:', familyUserObjects.length)
      } else if (Array.isArray(familyUsersData.data)) {
        familyUserObjects = familyUsersData.data
        console.log('Using data field, count:', familyUserObjects.length)
      } else {
        console.log('Unexpected data format:', familyUsersData)
      }
    } else {
      console.log('No valid data format found, familyUsersData:', familyUsersData)
    }
    
    console.log('Family user objects:', familyUserObjects)
    
    // 从家属用户中提取User信息
    const users: User[] = familyUserObjects.map(familyUser => {
      // 检查familyUser结构，可能直接包含user字段
      if (familyUser.user) {
        console.log('Extracting user from familyUser.user:', familyUser.user)
        return familyUser.user as User
      } else {
        // 如果没有user字段，尝试直接使用familyUser作为用户
        console.log('Using familyUser directly as user:', familyUser)
        return familyUser as User
      }
    })
    
    console.log('Extracted users:', users)
    console.log('Extracted users count:', users.length)
    
    // 验证提取的用户数据是否有效
    if (users.length === 0) {
      console.warn('No valid users extracted from family user data')
    } else {
      // 检查第一个用户的数据结构
      const firstUser = users[0]
      if (firstUser) {
        console.log('First user structure:', {
          id: firstUser.id,
          username: firstUser.username,
          real_name: firstUser.real_name,
          role: firstUser.role,
          hasRequiredFields: !!(firstUser.id && firstUser.username)
        })
      }
    }
    
    console.log('=== getFamilyUsers 完成 ===')
    return users
  } catch (error: any) {
    console.error('? Error in getFamilyUsers:', error)
    console.error('Error details:', error?.response?.data)
    console.error('Error status:', error?.response?.status)
    console.error('Error message:', error?.message)
    console.error('Error config:', error?.config)
    
    // 如果主要方法失败，尝试备用方案
    console.log('主要方法失败，尝试备用方案...')
    try {
      return await getAllUsersAndFilterFamily()
    } catch (backupError: any) {
      console.error('备用方案也失败了:', backupError)
      return []
    }
  }
}

// 或者直接获取所有用户，然后在前端过滤
// 这个函数作为备用方案
export async function getAllUsersAndFilterFamily(): Promise<User[]> {
  try {
    console.log('getAllUsersAndFilterFamily called')
    const allUsers = await getUsers()
    console.log('All users:', allUsers)
    
    // 过滤出家属用户
    const familyUsers = allUsers.filter(user => {
      const isFamily = user.role === 'family'
      console.log(`User ${user.id} (${user.username}) role: ${user.role}, isFamily: ${isFamily}`)
      return isFamily
    })
    
    console.log('Filtered family users:', familyUsers)
    return familyUsers
  } catch (error) {
    console.error('Error in getAllUsersAndFilterFamily:', error)
    return []
  }
}

// Staff specific functions  
export async function getStaffUsers(params?: Omit<UserQueryParams, 'role'>): Promise<User[]> {
  return getUsers({ ...params, role: 'staff' })
}

export async function getRelatedStaff(): Promise<User[]> {
  const data: any = await api.get('/family/related-staff/')
  if (Array.isArray(data)) {
    return data as User[]
  }
  // Handle DRF pagination or wrapped response
  if (data && typeof data === 'object' && 'results' in data && Array.isArray(data.results)) {
    return data.results as User[]
  }
  return []
}
