function showToast(message: string, type: 'success' | 'error' | 'warning' | 'info' = 'info', duration = 3000) {
  const existing = document.getElementById('app-toast')
  if (existing) existing.remove()

  const toast = document.createElement('div')
  toast.id = 'app-toast'
  
  const bgColor = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-gray-800'
  }[type]

  toast.className = `fixed top-5 left-1/2 -translate-x-1/2 ${bgColor} text-white px-6 py-3 rounded-lg shadow-lg z-[9999] text-sm font-medium transition-opacity duration-300 opacity-0`
  toast.textContent = message
  
  document.body.appendChild(toast)

  requestAnimationFrame(() => {
    toast.style.opacity = '1'
  })

  setTimeout(() => {
    toast.style.opacity = '0'
    setTimeout(() => {
      if (toast.parentNode) toast.parentNode.removeChild(toast)
    }, 300)
  }, duration)
}

export const Toast = {
  success: (msg: string) => showToast(msg, 'success'),
  error: (msg: string) => showToast(msg, 'error'),
  warning: (msg: string) => showToast(msg, 'warning'),
  info: (msg: string) => showToast(msg, 'info')
}

export default Toast
