import request from '../utils/request'

export function addHealthRecord(elderUserId: number, recordType: string, value: string) {
  return request.post('/health/records', {
    elder_user_id: elderUserId,
    record_type: recordType,
    value
  })
}

export function getHealthRecords(elderUserId: number, recordType?: string, limit: number = 30) {
  const params: any = { elder_user_id: elderUserId, limit }
  if (recordType) params.record_type = recordType
  return request.get('/health/records', { params })
}

export function getHealthSummary(elderUserId: number) {
  return request.get(`/health/summary/${elderUserId}`)
}