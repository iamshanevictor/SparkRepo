<template>
  <div class="login-container">
    <div class="login-form">
      <h2>Admin Login</h2>
      
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
          />
        </div>
        
        <button type="submit" class="login-btn" :disabled="loading">
          <span v-if="loading">
            <span class="spinner"></span> Logging in...
          </span>
          <span v-else>Login</span>
        </button>
      </form>
      
      <div class="back-to-app">
        <a href="#" @click.prevent="goToStudentView">Back to Student View</a>
      </div>
    </div>
  </div>
</template>

<script>
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
        const response = await fetch('http://localhost:5000/api/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.credentials)
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Login failed')
        }
        
        const data = await response.json()
        
        // Store token and user info in localStorage
        localStorage.setItem('auth_token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))
        
        // Emit login event
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
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 70vh;
}

.login-form {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  padding: 30px;
  width: 100%;
  max-width: 400px;
}

h2 {
  text-align: center;
  margin-bottom: 24px;
  color: #333;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.login-btn {
  width: 100%;
  padding: 12px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.login-btn:hover {
  background-color: #45a049;
}

.login-btn:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}

.error-message {
  background-color: #ffebee;
  color: #c62828;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.back-to-app {
  text-align: center;
  margin-top: 20px;
}

.back-to-app a {
  color: #2196F3;
  text-decoration: none;
}

.back-to-app a:hover {
  text-decoration: underline;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
