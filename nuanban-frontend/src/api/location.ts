import request from '../utils/request'

export function reportLocation(elderUserId: number, latitude: number, longitude: number, address?: string) {
  return request.post('/location/report', {
    elder_user_id: elderUserId,
    latitude,
    longitude,
    address
  })
}

export function getLatestLocation(elderUserId: number) {
  return request.get(`/location/latest/${elderUserId}`)
}

export function getLocationHistory(elderUserId: number, limit: number = 20) {
  return request.get(`/location/history/${elderUserId}`, { params: { limit } })
}
