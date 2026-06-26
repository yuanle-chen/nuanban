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
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router