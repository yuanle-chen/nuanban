import axios from 'axios'
import { useUserStore } from '../stores/user'
import router from '../router'
import Toast from './toast'

const request = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 10000
})

let isRefreshing = false
let refreshSubscribers: ((token: string) => void)[] = []

function subscribeTokenRefresh(callback: (token: string) => void) {
  refreshSubscribers.push(callback)
}

function onRefreshed(token: string) {
  refreshSubscribers.forEach(callback => callback(token))
  refreshSubscribers = []
}

async function refreshToken() {
  const userStore = useUserStore()
  try {
    const res: any = await axios.post(
      'http://localhost:8000/api/auth/refresh',
      {},
      {
        headers: {
          Authorization: `Bearer ${userStore.token}`
        }
      }
    )
    const newToken = res.data.access_token
    userStore.setToken(newToken, res.data.role || userStore.role || '')
    return newToken
  } catch (error) {
    userStore.logout()
    router.push('/login')
    throw error
  }
}

request.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

request.interceptors.response.use(
  (response) => response.data,
  async (error) => {
    const userStore = useUserStore()
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      if (isRefreshing) {
        return new Promise(resolve => {
          subscribeTokenRefresh((token: string) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            resolve(request(originalRequest))
          })
        })
      }

      originalRequest._retry = true
      isRefreshing = true

      try {
        const newToken = await refreshToken()
        onRefreshed(newToken)
        originalRequest.headers.Authorization = `Bearer ${newToken}`
        return request(originalRequest)
      } catch (refreshError) {
        return Promise.reject(refreshError)
      } finally {
        isRefreshing = false
      }
    }

    const message = error.response?.data?.detail || error.message || '请求失败'
    
    if (error.response?.status === 401) {
      Toast.error('登录已过期，请重新登录')
    } else if (error.response?.status === 403) {
      Toast.error('没有权限执行此操作')
    } else if (error.response?.status === 404) {
      Toast.error('请求的资源不存在')
    } else if (error.response?.status === 500) {
      Toast.error('服务器错误，请稍后重试')
    } else if (error.message === 'Network Error') {
      Toast.error('网络连接失败，请检查网络')
    } else {
      Toast.error(message)
    }

    console.error('请求错误:', error)
    return Promise.reject(error)
  }
)

export default request