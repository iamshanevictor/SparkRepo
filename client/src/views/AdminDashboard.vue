<script setup>
import AdminDashboard from '../components/AdminDashboard.vue'
import { useAuth } from '../composables/useAuth'
import { useRouter } from 'vue-router'

const { logout } = useAuth()
const router = useRouter()

function onLogout() {
  logout()
  router.push({ name: 'admin-login' })
}
</script>

<template>
  <AdminDashboard @logout="onLogout" />
</template>
