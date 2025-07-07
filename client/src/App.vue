<script>
import CategoryList from './components/CategoryList.vue'
import WeekView from './components/WeekView.vue'
import LoginForm from './components/LoginForm.vue'
import AdminDashboard from './components/AdminDashboard.vue'

export default {
  name: 'App',
  components: {
    CategoryList,
    WeekView,
    LoginForm,
    AdminDashboard
  },
  data() {
    return {
      currentView: 'categories',
      selectedCategory: null,
      selectedWeek: null,
      // Mock student ID for demo purposes
      // In a real app, this would come from authentication
      studentId: 1,
      // Admin authentication
      isAdmin: false,
      adminView: 'login',  // 'login' or 'dashboard'
      showAdminButton: true,

    }
  },
  created() {
    // Check if user is already logged in as admin
    const token = localStorage.getItem('auth_token')
    const user = localStorage.getItem('user')
    
    if (token && user) {
      try {
        const userData = JSON.parse(user)
        if (userData.is_admin) {
          this.isAdmin = true
          this.adminView = 'dashboard'
        }
      } catch (e) {
        // Invalid user data, clear storage
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user')
      }
    }
  },
  methods: {
    handleCategorySelected(categoryItem) {
      this.selectedCategory = categoryItem
      this.currentView = 'weeks'
      this.selectedWeek = 1 // Default to first week
    },
    goBackToCategories() {
      this.currentView = 'categories'
      this.selectedCategory = null
      this.selectedWeek = null
    },
    selectWeek(weekNumber) {
      this.selectedWeek = weekNumber
    },
    // Admin methods
    toggleAdminView() {
      this.isAdmin = !this.isAdmin
      this.adminView = 'login'
    },
    handleLoginSuccess(user) {
      this.adminView = 'dashboard'
    },
    handleLogout() {
      this.isAdmin = false
      this.adminView = 'login'
      this.currentView = 'categories'
    },
    goToStudentView() {
      this.isAdmin = false
      this.currentView = 'categories'
    }
  }
}
</script>

<template>
  <div class="app">
    <!-- Admin View -->
    <div v-if="isAdmin" class="admin-view">
      <LoginForm 
        v-if="adminView === 'login'" 
        @login-success="handleLoginSuccess"
        @go-to-student-view="goToStudentView"
      />
      <AdminDashboard 
        v-else 
        @logout="handleLogout"
      />
    </div>
    
    <!-- Student View -->
    <div v-else class="student-view">
      <header>
        <div class="logo-container">
          <img src="./assets/vue.svg" class="logo" alt="Vue logo" />
                    <h1>SparkRepo</h1>
        </div>
        <div class="header-right">
          <p class="tagline">Upload and share your Scratch projects</p>
          <button v-if="showAdminButton" class="admin-btn" @click="toggleAdminView">Admin</button>
        </div>
      </header>

      <main>
        <!-- Category Selection View -->
        <div v-if="currentView === 'categories'">
          <CategoryList 
            @category-selected="handleCategorySelected"
          />
        </div>
        
        <!-- Week View with Weeks Navigation -->
        <div v-else-if="currentView === 'weeks'" class="week-container">
          <div class="week-sidebar">
            <h3>Weeks</h3>
            <ul class="week-list">
              <li 
                v-for="weekNum in 10" 
                :key="weekNum"
                :class="{ active: selectedWeek === weekNum }"
                @click="selectWeek(weekNum)"
              >
                Week {{ weekNum }}
              </li>
            </ul>
          </div>
          
          <div class="week-content">
            <WeekView 
              :category-id="selectedCategory.id"
              :week-number="selectedWeek"
              :category-info="selectedCategory"
              :student-id="studentId"
              @go-back="goBackToCategories"
            />
          </div>
        </div>
      </main>
      
      <footer>
                <p>&copy; 2025 SparkRepo - A classroom link repository for Scratch projects</p>
      </footer>
    </div>
  </div>
</template>

<style>
/* Global styles */
:root {
  --primary-color: #4CAF50;
  --secondary-color: #2196F3;
  --background-color: #f5f7fa;
  --text-color: #333;
  --border-color: #e0e0e0;
  --admin-color: #673AB7;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--text-color);
  background-color: var(--background-color);
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Student view styles */
.student-view {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.logo {
  height: 3rem;
}

.tagline {
  color: #666;
  margin-bottom: 0.5rem;
}

.admin-btn {
  background-color: var(--admin-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.admin-btn:hover {
  background-color: #5e35b1;
}

main {
  flex: 1;
  padding: 2rem;
}

footer {
  background-color: #333;
  color: white;
  text-align: center;
  padding: 1rem;
  margin-top: auto;
}

/* Admin view styles */
.admin-view {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* Week view layout */
.week-container {
  display: flex;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.week-sidebar {
  flex: 0 0 200px;
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.week-content {
  flex: 1;
}

.week-list {
  list-style: none;
  margin-top: 1rem;
}

.week-list li {
  padding: 0.75rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 0.5rem;
  transition: background-color 0.2s;
}

.week-list li:hover {
  background-color: #f0f0f0;
}

.week-list li.active {
  background-color: var(--primary-color);
  color: white;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  header {
    flex-direction: column;
    text-align: center;
    padding: 1rem;
  }
  
  .header-right {
    margin-top: 1rem;
    align-items: center;
  }
  
  .week-container {
    flex-direction: column;
  }
  
  .week-sidebar {
    flex: none;
    width: 100%;
  }
  
  .week-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .week-list li {
    margin-bottom: 0;
  }
}
</style>
