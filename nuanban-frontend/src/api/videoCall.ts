import request from '../utils/request'

export function startVideoCall(receiverId: number) {
  return request.post('/video-call/start', { receiver_id: receiverId })
}

export function acceptCall(callId: number) {
  return request.post(`/video-call/${callId}/accept`)
}

export function endCall(callId: number) {
  return request.post(`/video-call/${callId}/end`)
}

export function getPendingCalls() {
  return request.get('/video-call/pending')
}

export function getCallHistory() {
  return request.get('/video-call/history')
}
