import request from '../utils/request'

export function login(username: string, password: string) {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)
  return request.post('/auth/login', formData)
}

export function register(data: { username: string; password: string; role: string; phone?: string }) {
  return request.post('/auth/register', data)
}

export function getCurrentUser() {
  return request.get('/auth/me')
}