<script setup>
import { useRouter } from 'vue-router'
import LoginForm from '../components/LoginForm.vue'

const router = useRouter()

function onLoginSuccess() {
  router.push({ name: 'admin-dashboard' })
}
</script>

<template>
  <div class="login-page">
    <h2>Admin Login</h2>
    <LoginForm @login-success="onLoginSuccess" />
  </div>
  </template>

<style scoped>
.login-page { max-width: 420px; margin: 5rem auto; padding: 2rem; background: #fff; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,.08); }
</style>
