import request from '../utils/request'

export function sendMessage(elderUserId: number, message: string) {
  return request.post('/chat/message', {
    elder_user_id: elderUserId,
    message
  })
}

export function getChatHistory(elderUserId: number, limit: number = 50) {
  return request.get('/chat/history', {
    params: { elder_user_id: elderUserId, limit }
  })
}
