import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomePage.vue')
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/LoginPage.vue')
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('../views/RegisterPage.vue')
  },
  {
    path: '/elder',
    name: 'ElderHome',
    component: () => import('../views/elder/ElderDashboard.vue')
  },
  {
    path: '/child',
    name: 'ChildHome',
    component: () => import('../views/child/ChildDashboard.vue')
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router