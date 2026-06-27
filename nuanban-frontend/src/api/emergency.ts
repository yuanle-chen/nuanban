import request from '../utils/request'

export function triggerSOS(elderUserId: number, alertType: string = 'sos', location?: string) {
  return request.post('/emergency/sos', {
    elder_user_id: elderUserId,
    alert_type: alertType,
    location
  })
}

export function cancelEmergency(recordId: number) {
  return request.put(`/emergency/cancel/${recordId}`)
}

export function getEmergencyHistory(elderUserId: number, limit: number = 20) {
  return request.get('/emergency/history', { params: { elder_user_id: elderUserId, limit } })
}

export function getPendingEmergencies() {
  return request.get('/emergency/pending')
}

export function handleEmergency(recordId: number, status: string) {
  return request.put('/emergency/handle/' + recordId, { handled_status: status })
}
