import request from '../utils/request'

export function getMedicationPlans(elderUserId: number) {
  return request.get('/medication/plans', { params: { elder_user_id: elderUserId } })
}

export function createMedicationPlan(data: {
  elder_user_id: number
  medication_name: string
  dosage: string
  frequency: string
  reminder_times: string[]
}) {
  return request.post('/medication/plans', data)
}

export function updateMedicationPlan(planId: number, data: {
  medication_name?: string
  dosage?: string
  frequency?: string
  reminder_times?: string[]
  is_active?: boolean
}) {
  return request.put(`/medication/plans/${planId}`, data)
}

export function getTodayMedication(elderUserId: number) {
  return request.get('/medication/today', { params: { elder_user_id: elderUserId } })
}

export function takeMedication(planId: number, scheduledTime: string, elderUserId: number) {
  return request.post('/medication/take', null, {
    params: { plan_id: planId, scheduled_time: scheduledTime, elder_user_id: elderUserId }
  })
}
