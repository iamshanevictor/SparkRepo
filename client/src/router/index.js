import { createRouter, createWebHistory } from 'vue-router'
import StudentHome from '../views/StudentHome.vue'
import WeekPage from '../views/WeekPage.vue'
import AdminLogin from '../views/AdminLogin.vue'
import AdminDashboardView from '../views/AdminDashboard.vue'
import { useAuth } from '../composables/useAuth'

const routes = [
  { path: '/', name: 'home', component: StudentHome },
  {
    path: '/category/:categoryId/week/:weekNumber',
    name: 'week',
    component: WeekPage,
    props: true,
  },
  { path: '/admin/login', name: 'admin-login', component: AdminLogin },
  {
    path: '/admin',
    name: 'admin-dashboard',
    component: AdminDashboardView,
    meta: { requiresAdmin: true },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, _from, next) => {
  const { isAuthenticated, isAdmin } = useAuth()
  if (to.meta.requiresAdmin) {
    if (!isAuthenticated() || !isAdmin()) {
      return next({ name: 'admin-login' })
    }
  }
  next()
})

export default router
