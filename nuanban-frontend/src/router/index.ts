import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '../stores/user'

const routes = [
  { path: '/', name: 'Home', component: () => import('../views/HomePage.vue'), meta: { public: true } },
  { path: '/login', name: 'Login', component: () => import('../views/LoginPage.vue'), meta: { public: true } },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterPage.vue'), meta: { public: true } },
  { path: '/forgot-password', name: 'ForgotPassword', component: () => import('../views/ForgotPasswordPage.vue'), meta: { public: true } },
  { path: '/elder', name: 'ElderHome', component: () => import('../views/elder/ElderDashboard.vue'), meta: { requiresAuth: true, role: 'elder' } },
  { path: '/child', name: 'ChildHome', component: () => import('../views/child/ChildDashboard.vue'), meta: { requiresAuth: true, role: 'child' } },
  { path: '/child/bind', name: 'BindElder', component: () => import('../views/child/BindElderPage.vue'), meta: { requiresAuth: true, role: 'child' } },
  { path: '/child/profile', name: 'ElderProfile', component: () => import('../views/child/ElderProfilePage.vue'), meta: { requiresAuth: true, role: 'child' } },
  { path: '/elder/health', name: 'ElderHealth', component: () => import('../views/elder/HealthRecordPage.vue'), meta: { requiresAuth: true, role: 'elder' } },
  { path: '/child/report', name: 'ChildHealthReport', component: () => import('../views/child/HealthReportPage.vue'), meta: { requiresAuth: true, role: 'child' } },
  { path: '/elder/medication', name: 'ElderMedication', component: () => import('../views/elder/MedicationPage.vue'), meta: { requiresAuth: true, role: 'elder' } },
  { path: '/child/medication', name: 'ChildMedication', component: () => import('../views/child/MedicationSettingsPage.vue'), meta: { requiresAuth: true, role: 'child' } },
  { path: '/elder/emergency', name: 'ElderEmergency', component: () => import('../views/elder/EmergencyPage.vue'), meta: { requiresAuth: true, role: 'elder' } },
  { path: '/child/alerts', name: 'ChildAlerts', component: () => import('../views/child/EmergencyAlertsPage.vue'), meta: { requiresAuth: true, role: 'child' } },
  { path: '/elder/chat', name: 'ElderChat', component: () => import('../views/elder/ChatPage.vue'), meta: { requiresAuth: true, role: 'elder' } },
  { path: '/elder/profile', name: 'ElderProfilePage', component: () => import('../views/elder/ElderProfilePage.vue'), meta: { requiresAuth: true, role: 'elder' } },
  { path: '/child/settings', name: 'ChildSettings', component: () => import('../views/child/SettingsPage.vue'), meta: { requiresAuth: true, role: 'child' } },
  { path: '/child/status', name: 'ChildStatus', component: () => import('../views/child/StatusPage.vue'), meta: { requiresAuth: true, role: 'child' } },
  { path: '/child/video-call', name: 'ChildVideoCall', component: () => import('../views/child/VideoCallPage.vue'), meta: { requiresAuth: true, role: 'child' } },
  { path: '/elder/video-call', name: 'ElderVideoCall', component: () => import('../views/elder/VideoCallPage.vue'), meta: { requiresAuth: true, role: 'elder' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const userStore = useUserStore()
  const token = userStore.token
  const role = userStore.role

  if (to.meta.public) {
    if (token && to.path === '/login') {
      if (role === 'elder') next('/elder')
      else if (role === 'child') next('/child')
      else next()
    } else {
      next()
    }
    return
  }

  if (to.meta.requiresAuth) {
    if (!token) {
      const role = to.meta.role || ''
      next({ path: '/login', query: { redirect: to.fullPath, ...(role && { role }) } })
      return
    }

    if (to.meta.role && role !== to.meta.role) {
      if (role === 'elder') next('/elder')
      else if (role === 'child') next('/child')
      else next({ path: '/login', query: { role: to.meta.role } })
      return
    }

    next()
    return
  }

  next()
})

export default router