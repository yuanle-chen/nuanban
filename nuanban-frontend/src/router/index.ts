import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  { path: '/', name: 'Home', component: () => import('../views/HomePage.vue') },
  { path: '/login', name: 'Login', component: () => import('../views/LoginPage.vue') },
  { path: '/register', name: 'Register', component: () => import('../views/RegisterPage.vue') },
  { path: '/elder', name: 'ElderHome', component: () => import('../views/elder/ElderDashboard.vue') },
  { path: '/child', name: 'ChildHome', component: () => import('../views/child/ChildDashboard.vue') },
  // 新增：绑定老人页面
  { path: '/child/bind', name: 'BindElder', component: () => import('../views/child/BindElderPage.vue') },
  // 新增：老人档案页面
  { path: '/child/profile', name: 'ElderProfile', component: () => import('../views/child/ElderProfilePage.vue') },
// 老人端 - 健康记录
{ path: '/elder/health', name: 'ElderHealth', component: () => import('../views/elder/HealthRecordPage.vue') },
// 子女端 - 健康报告
{ path: '/child/report', name: 'ChildHealthReport', component: () => import('../views/child/HealthReportPage.vue') },
// 老人端 - 用药提醒
{ path: '/elder/medication', name: 'ElderMedication', component: () => import('../views/elder/MedicationPage.vue') },
// 子女端 - 用药设置
{ path: '/child/medication', name: 'ChildMedication', component: () => import('../views/child/MedicationSettingsPage.vue') },
// 老人端 - 紧急求助
{ path: '/elder/emergency', name: 'ElderEmergency', component: () => import('../views/elder/EmergencyPage.vue') },
// 子女端 - 紧急求助列表
{ path: '/child/alerts', name: 'ChildAlerts', component: () => import('../views/child/EmergencyAlertsPage.vue') },
// 老人端 - AI聊天
{ path: '/elder/chat', name: 'ElderChat', component: () => import('../views/elder/ChatPage.vue') },
// 老人端 - 个人中心
{ path: '/elder/profile', name: 'ElderProfilePage', component: () => import('../views/elder/ElderProfilePage.vue') },
// 子女端 - 设置
{ path: '/child/settings', name: 'ChildSettings', component: () => import('../views/child/SettingsPage.vue') },
// 子女端 - 实时状态
{ path: '/child/status', name: 'ChildStatus', component: () => import('../views/child/StatusPage.vue') },

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router