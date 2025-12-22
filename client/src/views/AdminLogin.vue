<script setup>
import { useRouter } from 'vue-router'
import LoginForm from '../components/LoginForm.vue'

const router = useRouter()

function onLoginSuccess() {
  router.push({ name: 'admin-dashboard' })
}
</script>

<template>
  <div class="login-container">
    <div class="login-page">
      <div class="login-header">
        <h2>Instructor Portal</h2>
        <p>Access your administrative dashboard</p>
      </div>
      <LoginForm @login-success="onLoginSuccess" />
    </div>
  </div>
</template>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.login-page {
  max-width: 440px;
  width: 100%;
  background: white;
  border-radius: 12px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  padding: 2.5rem;
}

.login-header {
  text-align: center;
  margin-bottom: 2rem;
}

.login-header h2 {
  font-size: 1.875rem;
  font-weight: 700;
  color: #1e3c72;
  margin: 0 0 0.5rem 0;
}

.login-header p {
  color: #6b7280;
  font-size: 0.95rem;
  margin: 0;
}
</style>
