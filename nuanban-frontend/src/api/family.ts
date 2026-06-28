import request from '../utils/request'

export function bindElder(elderUserId: number, relationType: string = '子女') {
  return request.post('/family/bind', { elder_user_id: elderUserId, relation_type: relationType })
}

export function bindElderByPhone(phone: string, relationType: string = '子女') {
  return request.post('/family/bind-by-phone', { phone, relation_type: relationType })
}

export function getMyElders() {
  return request.get('/family/elders')
}

export function getMyChildren() {
  return request.get('/family/children')
}

export function getElderProfile(userId: number) {
  return request.get(`/family/profile/${userId}`)
}

export function createElderProfile(data: {
  user_id: number
  real_name: string
  age?: number
  gender?: string
  address?: string
  emergency_contact?: string
  emergency_phone?: string
}) {
  return request.post('/family/profile', data)
}

export function updateElderProfile(userId: number, data: {
  real_name?: string
  age?: number
  gender?: string
  address?: string
  emergency_contact?: string
  emergency_phone?: string
}) {
  return request.put(`/family/profile/${userId}`, data)
}

export function getElderAlerts(elderUserId: number) {
  return request.get(`/family/alerts/${elderUserId}`)
}

export function unbindElder(elderUserId: number) {
  return request.delete(`/family/unbind/${elderUserId}`)
}