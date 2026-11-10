import { createRouter, createWebHistory } from 'vue-router'
import AdminLayout from '../layouts/AdminLayout.vue'
import Dashboard from '../views/Dashboard.vue'
import Products from '../views/Products.vue'
import Brands from '../views/Brands.vue'
import Orders from '../views/Orders.vue'
import Users from '../views/Users.vue'
import AuditLogs from '../views/AuditLogs.vue'
import Login from '../views/Login.vue'
import Storefront from '../views/Storefront.vue'
import NotFound from '../views/NotFound.vue'

const routes = [
  {
    path: '/',
    name: 'Storefront',
    component: Storefront
  },
  {
    path: '/admin',
    component: AdminLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/admin/dashboard'
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: Dashboard
      },
      {
        path: 'products',
        name: 'Produk',
        component: Products
      },
      {
        path: 'brands',
        name: 'Merek',
        component: Brands
      },
      {
        path: 'orders',
        name: 'Pesanan',
        component: Orders
      },
      {
        path: 'users',
        name: 'Pengguna',
        component: Users
      },
      {
        path: 'audit-logs',
        name: 'Audit Keamanan (A5)',
        component: AuditLogs
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard for Authentication
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/admin/dashboard')
  } else {
    next()
  }
})

export default router
