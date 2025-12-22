<template>
  <div class="login-form">
    <div v-if="error" class="error-message">{{ error }}</div>
    
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username</label>
        <input 
          type="text" 
          id="username" 
          v-model="credentials.username" 
          required
          :disabled="loading"
          placeholder="Enter your username"
        />
      </div>
      
      <div class="form-group">
        <label for="password">Password</label>
        <input 
          type="password" 
          id="password" 
          v-model="credentials.password" 
          required
          :disabled="loading"
          placeholder="Enter your password"
        />
      </div>
      
      <button type="submit" class="login-btn" :disabled="loading">
        <span v-if="loading">
          <span class="spinner"></span> Signing in...
        </span>
        <span v-else>Sign In</span>
      </button>
    </form>
    
    <div class="back-to-app">
      <a href="/" @click.prevent="$router.push('/')">← Back to Student Portal</a>
    </div>
  </div>
</template>

<script>
import { api } from '../api'
import { useAuth } from '../composables/useAuth'

export default {
  name: 'LoginForm',
  data() {
    return {
      credentials: {
        username: '',
        password: ''
      },
      loading: false,
      error: null
    }
  },
  methods: {
    async login() {
      this.loading = true
      this.error = null
      
      try {
        const data = await api.login(this.credentials.username, this.credentials.password)
        const { login } = useAuth()
        login(data.access_token, data.user)
        this.$emit('login-success', data.user)
      } catch (err) {
        this.error = err.message
        console.error('Login error:', err)
      } finally {
        this.loading = false
      }
    },
    goToStudentView() {
      this.$emit('go-to-student-view')
    }
  }
}
</script>

<style scoped>
.login-form {
  width: 100%;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
  font-size: 0.925rem;
}

input {
  width: 100%;
  padding: 0.875rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
  font-family: inherit;
}

input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

input::placeholder {
  color: #9ca3af;
}

input:disabled {
  background: #f9fafb;
  cursor: not-allowed;
}

.login-btn {
  width: 100%;
  padding: 0.875rem 1.5rem;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  margin-top: 0.5rem;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(30, 60, 114, 0.3);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.error-message {
  background: #fee2e2;
  color: #991b1b;
  padding: 0.875rem 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-size: 0.925rem;
  font-weight: 500;
  border-left: 4px solid #dc2626;
}

.back-to-app {
  text-align: center;
  margin-top: 1.75rem;
  padding-top: 1.5rem;
  border-top: 1px solid #e5e7eb;
}

.back-to-app a {
  color: #3b82f6;
  text-decoration: none;
  font-weight: 500;
  font-size: 0.925rem;
  transition: color 0.2s;
}

.back-to-app a:hover {
  color: #2563eb;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 0.8s linear infinite;
  margin-right: 0.5rem;
  vertical-align: middle;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
