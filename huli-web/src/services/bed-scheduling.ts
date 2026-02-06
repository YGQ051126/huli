import api from './api'

export interface Bed {
  id: string
  roomNumber: string
  bedNumber: string

  status: 'available' | 'occupied' | 'cleaning' | 'maintenance'
  elderlyId?: string
  elderlyName?: string
  lastUpdated?: string
}

export interface BedStatus {
  totalBeds: number
  available: number
  occupied: number
  cleaning: number
  maintenance: number
  beds: Bed[]
}

export interface MatchedBed {
  id: string
  roomNumber: string
  bedNumber: string
  building?: string
  floor?: number
  matchScore: number
  reason: string
}

export interface BedMatchResult {
  matchedBeds: MatchedBed[]
  recommendedBed: MatchedBed
}

export interface BedAssignment {
  id: string
  elderlyId: string
  elderlyName: string
  bedId: string
  roomNumber: string
  bedNumber: string
  assignDate: string
  status: string
  cleaningNotified: boolean
  createdAt: string
}

export interface MatchBedData {
  elderlyId: string
  nursingLevel: string
  preferredBuilding?: string
  preferredFloor?: number
}

export interface AssignBedData {
  elderlyId: string
  bedId: string
  assignDate: string
}

export interface BedAllocationHistory {
  id: string
  elderlyId: string
  elderlyName: string
  bedId: string
  roomNumber: string
  bedNumber: string
  assignDate: string
  releaseDate?: string
  assignedBy: string
  status: 'active' | 'completed' | 'cancelled'
  notes?: string
  createdAt: string
}

export interface CleaningNotification {
  id: string
  bedId: string
  roomNumber: string
  bedNumber: string
  message: string
  status: 'pending' | 'sent' | 'failed'
  sentAt?: string
  createdAt: string
}

function assertBedStatusShape(value: any): asserts value is BedStatus {
  const ok =
    value &&
    typeof value === 'object' &&
    typeof value.totalBeds === 'number' &&
    typeof value.available === 'number' &&
    typeof value.occupied === 'number' &&
    typeof value.cleaning === 'number' &&
    typeof value.maintenance === 'number' &&
    Array.isArray(value.beds)
  if (!ok) {
    console.error('[bed_scheduling] 数据格式错误: BedStatus 结构不匹配', value)
    throw new Error('数据格式错误')
  }
}

export async function getBedStatus(building?: string, floor?: number, status?: string): Promise<BedStatus> {
  console.groupCollapsed('[bed_scheduling] getBedStatus')
  console.log('params:', { building, floor, status })
  try {
    const data = (await api.get('/bed_scheduling/beds/status/', {
      params: { building, floor, status }
    })) as unknown as BedStatus
    assertBedStatusShape(data)
    console.log('result:', { totalBeds: data.totalBeds, beds: data.beds.length })
    return data
  } finally {
    console.groupEnd()
  }
}

export async function getBedByRoomNumber(roomNumber: string): Promise<Bed[]> {
  const data = (await api.get('/bed_scheduling/beds/', {
    params: { room_number: roomNumber }
  })) as unknown as Bed[]
  return data
}

export async function matchBed(data: MatchBedData): Promise<BedMatchResult> {
  const resp = (await api.post('/bed_scheduling/beds/match/', data)) as unknown as BedMatchResult
  return resp
}

export async function assignBed(data: AssignBedData): Promise<BedAssignment> {
  const resp = (await api.post('/bed_scheduling/assignments/', data)) as unknown as BedAssignment
  return resp
}

export async function getAllocationHistory(elderlyId?: string, bedId?: string): Promise<BedAllocationHistory[]> {
  const data = (await api.get('/bed_scheduling/assignments/', {
    params: { elderly_id: elderlyId, bed_id: bedId }
  })) as unknown as BedAllocationHistory[]
  return data
}

export async function getCleaningNotifications(bedId?: string): Promise<CleaningNotification[]> {
  const data = (await api.get('/bed_scheduling/cleaning-requests/', {
    params: { bed_id: bedId }
  })) as unknown as CleaningNotification[]
  return data
}

export async function sendCleaningNotification(bedId: string): Promise<CleaningNotification> {
  const data = (await api.post('/bed_scheduling/cleaning-requests/', { bed_id: bedId })) as unknown as CleaningNotification
  return data
}

export async function updateBedStatus(bedId: string, status: Bed['status']): Promise<Bed> {
  const data = (await api.patch(`/bed_scheduling/beds/${bedId}/set_status/`, { status })) as unknown as Bed
  return data
}

export async function generateAllocationForm(assignmentId: string): Promise<Blob> {
  const res = await api.get(`/bed_scheduling/assignments/${assignmentId}/form/`, {
    responseType: 'blob'
  })
  // Handle case where API wrapper might wrap response
  // If api wrapper returns data directly for blob, it's fine.
  // But our api wrapper (axios) returns response.data
  return res as unknown as Blob
}
