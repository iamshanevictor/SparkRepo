<template>
  <div class="admin-dashboard">
    <div class="admin-header">
      <h2>Admin Dashboard</h2>
      <button class="logout-btn" @click="logout">Logout</button>
    </div>
    
    <div class="admin-tabs">
      <button 
        :class="['tab-btn', { active: activeTab === 'weeks' }]" 
        @click="activeTab = 'weeks'"
      >
        Manage Weeks
      </button>
      <button 
        :class="['tab-btn', { active: activeTab === 'submissions' }]" 
        @click="activeTab = 'submissions'"
      >
        Manage Submissions
      </button>

    </div>
    
    <!-- Weeks Management Tab -->
    <div v-if="activeTab === 'weeks'" class="tab-content">
      <div class="section-header">
        <h3>Weeks Management</h3>
        <button class="add-btn" @click="showAddWeekForm = true">Add New Week</button>
      </div>
      
      <div v-if="loading.weeks" class="loading">Loading weeks...</div>
      <div v-else-if="error.weeks" class="error">{{ error.weeks }}</div>
      <div v-else class="weeks-list">
        <table>
          <thead>
            <tr>
              <th>Week #</th>
              <th>Class</th>
              <th>Title</th>
              <th>Display Name</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="week in weeks" :key="week.id">
              <td>{{ week.week_number }}</td>
              <td>{{ week.class_name }}</td>
              <td>{{ week.title }}</td>
              <td>{{ week.display_name }}</td>
              <td>
                <span :class="['status', week.is_active ? 'active' : 'inactive']">
                  {{ week.is_active ? 'Active' : 'Inactive' }}
                </span>
              </td>
              <td>
                <button class="edit-btn" @click="editWeek(week)">Edit</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Edit Week Modal -->
      <div v-if="showEditWeekForm" class="modal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Edit Week</h3>
            <button class="close-btn" @click="showEditWeekForm = false">&times;</button>
          </div>
          
          <form @submit.prevent="updateWeek">
            <div class="form-group">
              <label for="title">Title</label>
              <input type="text" id="title" v-model="editingWeek.title" required />
            </div>
            
            <div class="form-group">
              <label for="display-name">Display Name (optional)</label>
              <input type="text" id="display-name" v-model="editingWeek.display_name" />
              <small>This will be shown to students instead of the title if provided</small>
            </div>
            
            <div class="form-group">
              <label for="description">Description</label>
              <textarea id="description" v-model="editingWeek.description" rows="3"></textarea>
            </div>
            
            <div class="form-group">
              <label for="assignment-url">Assignment URL</label>
              <input type="url" id="assignment-url" v-model="editingWeek.assignment_url" />
            </div>
            
            <div class="form-group">
              <label for="due-date">Due Date</label>
              <input type="datetime-local" id="due-date" v-model="editingWeek.due_date_local" />
            </div>
            
            <div class="form-group">
              <label class="checkbox-label">
                <input type="checkbox" v-model="editingWeek.is_active" />
                Active
              </label>
              <small>Inactive weeks won't be visible to students</small>
            </div>
            
            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="showEditWeekForm = false">Cancel</button>
              <button type="submit" class="save-btn" :disabled="loading.updateWeek">
                <span v-if="loading.updateWeek">Saving...</span>
                <span v-else>Save Changes</span>
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <!-- Add Week Modal -->
      <div v-if="showAddWeekForm" class="modal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Add New Week</h3>
            <button class="close-btn" @click="showAddWeekForm = false">&times;</button>
          </div>
          
          <form @submit.prevent="addWeek">
            <div class="form-group">
              <label for="new-class">Class</label>
              <select id="new-class" v-model="newWeek.class_id" required>
                <option v-for="cls in classes" :key="cls.id" :value="cls.id">
                  {{ cls.name }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="new-week-number">Week Number</label>
              <input type="number" id="new-week-number" v-model.number="newWeek.week_number" min="1" required />
            </div>
            
            <div class="form-group">
              <label for="new-title">Title</label>
              <input type="text" id="new-title" v-model="newWeek.title" required />
            </div>
            
            <div class="form-group">
              <label for="new-display-name">Display Name (optional)</label>
              <input type="text" id="new-display-name" v-model="newWeek.display_name" />
            </div>
            
            <div class="form-group">
              <label for="new-description">Description</label>
              <textarea id="new-description" v-model="newWeek.description" rows="3"></textarea>
            </div>
            
            <div class="form-group">
              <label for="new-assignment-url">Assignment URL</label>
              <input type="url" id="new-assignment-url" v-model="newWeek.assignment_url" />
            </div>
            
            <div class="form-group">
              <label for="new-due-date">Due Date</label>
              <input type="datetime-local" id="new-due-date" v-model="newWeek.due_date_local" />
            </div>
            
            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="showAddWeekForm = false">Cancel</button>
              <button type="submit" class="save-btn" :disabled="loading.addWeek">
                <span v-if="loading.addWeek">Adding...</span>
                <span v-else>Add Week</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
    
    <!-- Submissions Management Tab -->
    <div v-if="activeTab === 'submissions'" class="tab-content">
      <div class="section-header">
        <h3>Submissions Management</h3>
        <div class="filters">
          <select v-model="filters.class_id" @change="fetchSubmissions">
            <option value="">All Classes</option>
            <option v-for="cls in classes" :key="cls.id" :value="cls.id">
              {{ cls.name }}
            </option>
          </select>
          
          <select v-model="filters.week_id" @change="fetchSubmissions">
            <option value="">All Weeks</option>
            <option v-for="week in weeks" :key="week.id" :value="week.id">
              Week {{ week.week_number }}: {{ week.display_name || week.title }}
            </option>
          </select>
          
          <select v-model="filters.status" @change="fetchSubmissions">
            <option value="">All Statuses</option>
            <option value="submitted">Submitted</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>
      </div>
      
      <div v-if="loading.submissions" class="loading">Loading submissions...</div>
      <div v-else-if="error.submissions" class="error">{{ error.submissions }}</div>
      <div v-else-if="submissions.length === 0" class="no-data">
        No submissions found with the current filters.
      </div>
      <div v-else class="submissions-list">
        <table>
          <thead>
            <tr>
              <th>Student</th>
              <th>Week</th>
              <th>Project URL</th>
              <th>Status</th>
              <th>Submitted</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="sub in submissions" :key="sub.id">
              <td>{{ sub.student_name }}</td>
              <td>Week {{ sub.week_number }}: {{ sub.week_title }}</td>
              <td>
                <a :href="sub.project_url" target="_blank" rel="noopener noreferrer">
                  {{ sub.project_url.substring(0, 30) }}...
                </a>
              </td>
              <td>
                <span :class="['status', sub.status]">
                  {{ sub.status.charAt(0).toUpperCase() + sub.status.slice(1) }}
                </span>
              </td>
              <td>{{ formatDate(sub.submitted_at) }}</td>
              <td>
                <button class="edit-btn" @click="editSubmission(sub)">Review</button>
                <button class="delete-btn" @click="confirmDeleteSubmission(sub)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Edit Submission Modal -->
      <div v-if="showEditSubmissionForm" class="modal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Review Submission</h3>
            <button class="close-btn" @click="showEditSubmissionForm = false">&times;</button>
          </div>
          
          <div class="submission-details">
            <div class="detail-row">
              <strong>Student:</strong> {{ editingSubmission.student_name }}
            </div>
            <div class="detail-row">
              <strong>Week:</strong> Week {{ editingSubmission.week_number }}: {{ editingSubmission.week_title }}
            </div>
            <div class="detail-row">
              <strong>Project URL:</strong> 
              <a :href="editingSubmission.project_url" target="_blank" rel="noopener noreferrer">
                {{ editingSubmission.project_url }}
              </a>
            </div>
            <div class="detail-row">
              <strong>Student Comment:</strong> 
              <p>{{ editingSubmission.comment || 'No comment provided' }}</p>
            </div>
            <div class="detail-row">
              <strong>Submitted:</strong> {{ formatDate(editingSubmission.submitted_at) }}
            </div>
          </div>
          
          <form @submit.prevent="updateSubmission">
            <div class="form-group">
              <label for="submission-status">Status</label>
              <select id="submission-status" v-model="editingSubmission.status" required>
                <option value="submitted">Submitted</option>
                <option value="approved">Approved</option>
                <option value="rejected">Rejected</option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="admin-comment">Admin Comment</label>
              <textarea id="admin-comment" v-model="editingSubmission.admin_comment" rows="3"></textarea>
            </div>
            
            <div class="form-actions">
              <button type="button" class="cancel-btn" @click="showEditSubmissionForm = false">Cancel</button>
              <button type="submit" class="save-btn" :disabled="loading.updateSubmission">
                <span v-if="loading.updateSubmission">Saving...</span>
                <span v-else>Save Changes</span>
              </button>
            </div>
          </form>
        </div>
      </div>
      
      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteConfirmation" class="modal">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Confirm Deletion</h3>
            <button class="close-btn" @click="showDeleteConfirmation = false">&times;</button>
          </div>
          
          <div class="confirmation-message">
            <p>Are you sure you want to delete this submission?</p>
            <p><strong>Student:</strong> {{ deletingSubmission.student_name }}</p>
            <p><strong>Week:</strong> Week {{ deletingSubmission.week_number }}</p>
            <p>This action cannot be undone.</p>
          </div>
          
          <div class="form-actions">
            <button type="button" class="cancel-btn" @click="showDeleteConfirmation = false">Cancel</button>
            <button type="button" class="delete-btn" @click="deleteSubmission" :disabled="loading.deleteSubmission">
              <span v-if="loading.deleteSubmission">Deleting...</span>
              <span v-else>Delete</span>
            </button>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script>
export default {
  name: 'AdminDashboard',
  data() {
    return {
      activeTab: 'weeks',
      weeks: [],
      classes: [],
      submissions: [],
      filters: {
        class_id: '',
        week_id: '',
        status: ''
      },
      loading: {
        weeks: false,
        classes: false,
        submissions: false,
        updateWeek: false,
        addWeek: false,
        updateSubmission: false,
        deleteSubmission: false,
      },
      error: {
        weeks: null,
        classes: null,
        submissions: null,
      },
      showEditWeekForm: false,
      showAddWeekForm: false,
      showEditSubmissionForm: false,
      showDeleteConfirmation: false,
      editingWeek: null,
      editingSubmission: null,
      deletingSubmission: null,
      newWeek: {
        class_id: '',
        week_number: 1,
        title: '',
        display_name: '',
        description: '',
        assignment_url: '',
        due_date_local: ''
      }
    }
  },
  mounted() {
    this.fetchClasses()
    this.fetchWeeks()
    this.fetchSubmissions()
  },
  methods: {
    // Authentication
    getAuthHeaders() {
      const token = localStorage.getItem('auth_token')
      return {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    },
    logout() {
      localStorage.removeItem('auth_token')
      localStorage.removeItem('user')
      this.$emit('logout')
    },
    
    // Data fetching
    async fetchClasses() {
      this.loading.classes = true
      this.error.classes = null
      
      try {
        const response = await fetch('http://localhost:5000/api/classes', {
          headers: this.getAuthHeaders()
        })
        
        if (!response.ok) {
          throw new Error('Failed to fetch classes')
        }
        
        const data = await response.json()
        this.classes = data
      } catch (err) {
        this.error.classes = err.message
        console.error('Error fetching classes:', err)
      } finally {
        this.loading.classes = false
      }
    },
    
    async fetchWeeks() {
      this.loading.weeks = true
      this.error.weeks = null
      
      try {
        const response = await fetch('http://localhost:5000/api/admin/weeks', {
          headers: this.getAuthHeaders()
        })
        
        if (!response.ok) {
          throw new Error('Failed to fetch weeks')
        }
        
        const data = await response.json()
        this.weeks = data.weeks
      } catch (err) {
        this.error.weeks = err.message
        console.error('Error fetching weeks:', err)
      } finally {
        this.loading.weeks = false
      }
    },
    
    async fetchSubmissions() {
      this.loading.submissions = true
      this.error.submissions = null
      
      try {
        // Build query string from filters
        const queryParams = new URLSearchParams()
        if (this.filters.class_id) queryParams.append('class_id', this.filters.class_id)
        if (this.filters.week_id) queryParams.append('week_id', this.filters.week_id)
        if (this.filters.status) queryParams.append('status', this.filters.status)
        
        const url = `http://localhost:5000/api/admin/submissions?${queryParams.toString()}`
        
        const response = await fetch(url, {
          headers: this.getAuthHeaders()
        })
        
        if (!response.ok) {
          throw new Error('Failed to fetch submissions')
        }
        
        const data = await response.json()
        this.submissions = data.submissions
      } catch (err) {
        this.error.submissions = err.message
        console.error('Error fetching submissions:', err)
      } finally {
        this.loading.submissions = false
      }
    },
    
    formatDate(isoString) {
      if (!isoString) return 'N/A';
      const date = new Date(isoString);
      return date.toLocaleString();
    },

    // Week management
    editWeek(week) {
      // Convert ISO date string to local datetime-local format
      const dueDate = week.due_date ? new Date(week.due_date) : null
      const dueDateLocal = dueDate ? 
        new Date(dueDate.getTime() - dueDate.getTimezoneOffset() * 60000)
          .toISOString()
          .slice(0, 16) : ''
      
      this.editingWeek = {
        ...week,
        due_date_local: dueDateLocal
      }
      this.showEditWeekForm = true
    },
    
    async updateWeek() {
      this.loading.updateWeek = true
      
      try {
        // Convert local date back to ISO format
        const weekData = {
          ...this.editingWeek
        }
        
        if (weekData.due_date_local) {
          weekData.due_date = new Date(weekData.due_date_local).toISOString()
        }
        
        // Remove fields that shouldn't be sent
        delete weekData.due_date_local
        delete weekData.class_name
        
        const response = await fetch(`http://localhost:5000/api/admin/weeks/${this.editingWeek.id}`, {
          method: 'PUT',
          headers: this.getAuthHeaders(),
          body: JSON.stringify(weekData)
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Failed to update week')
        }
        
        // Refresh weeks list
        await this.fetchWeeks()
        this.showEditWeekForm = false
      } catch (err) {
        console.error('Error updating week:', err)
        alert(`Error: ${err.message}`)
      } finally {
        this.loading.updateWeek = false
      }
    },
    
    async addWeek() {
      this.loading.addWeek = true
      
      try {
        // Convert local date to ISO format
        const weekData = {
          ...this.newWeek
        }
        
        if (weekData.due_date_local) {
          weekData.due_date = new Date(weekData.due_date_local).toISOString()
        }
        
        // Remove fields that shouldn't be sent
        delete weekData.due_date_local
        
        const response = await fetch(`http://localhost:5000/api/admin/classes/${this.newWeek.class_id}/weeks`, {
          method: 'POST',
          headers: this.getAuthHeaders(),
          body: JSON.stringify(weekData)
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Failed to add week')
        }
        
        // Refresh weeks list
        await this.fetchWeeks()
        
        // Reset form and close modal
        this.newWeek = {
          class_id: '',
          week_number: 1,
          title: '',
          display_name: '',
          description: '',
          assignment_url: '',
          due_date_local: ''
        }
        this.showAddWeekForm = false
      } catch (err) {
        console.error('Error adding week:', err)
        alert(`Error: ${err.message}`)
      } finally {
        this.loading.addWeek = false
      }
    },
    
    // Submission management
    editSubmission(submission) {
      this.editingSubmission = { ...submission }
      this.showEditSubmissionForm = true
    },
    
    async updateSubmission() {
      this.loading.updateSubmission = true
      
      try {
        const submissionData = {
          status: this.editingSubmission.status,
          admin_comment: this.editingSubmission.admin_comment
        }
        
        const response = await fetch(`http://localhost:5000/api/admin/submissions/${this.editingSubmission.id}`, {
          method: 'PUT',
          headers: this.getAuthHeaders(),
          body: JSON.stringify(submissionData)
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Failed to update submission')
        }
        
        // Refresh submissions list
        await this.fetchSubmissions()
        this.showEditSubmissionForm = false
      } catch (err) {
        console.error('Error updating submission:', err)
        alert(`Error: ${err.message}`)
      } finally {
        this.loading.updateSubmission = false
      }
    },
    
    confirmDeleteSubmission(submission) {
      this.deletingSubmission = submission
      this.showDeleteConfirmation = true
    },
    
    async deleteSubmission() {
      this.loading.deleteSubmission = true
      
      try {
        const response = await fetch(`http://localhost:5000/api/admin/submissions/${this.deletingSubmission.id}`, {
          method: 'DELETE',
          headers: this.getAuthHeaders()
        })
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Failed to delete submission')
        }
        
        // Refresh submissions list
        await this.fetchSubmissions()
        this.showDeleteConfirmation = false
      } catch (err) {
        console.error('Error deleting submission:', err)
        alert(`Error: ${err.message}`)
      } finally {
        this.loading.deleteSubmission = false
      }
    },
    
    // Utility functions
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.admin-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.logout-btn {
  background-color: #f44336;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.admin-tabs {
  display: flex;
  margin-bottom: 20px;
  border-bottom: 1px solid #ddd;
}

.tab-btn {
  padding: 10px 20px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 16px;
  border-bottom: 3px solid transparent;
  color: #555;
}

.tab-btn.active {
  border-bottom-color: #4CAF50;
  font-weight: bold;
  color: #000;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.add-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}

th {
  background-color: #f5f5f5;
  font-weight: bold;
}

.status {
  display: inline-block;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 14px;
}

.status.active {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status.inactive {
  background-color: #f5f5f5;
  color: #757575;
}

.status.submitted {
  background-color: #e3f2fd;
  color: #1565c0;
}

.status.approved {
  background-color: #e8f5e9;
  color: #2e7d32;
}

.status.rejected {
  background-color: #ffebee;
  color: #c62828;
}

.edit-btn, .delete-btn {
  padding: 4px 8px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-right: 5px;
}

.edit-btn {
  background-color: #2196F3;
  color: white;
}

.delete-btn {
  background-color: #f44336;
  color: white;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

input, select, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 16px;
}

.checkbox-label {
  display: flex;
  align-items: center;
}

.checkbox-label input {
  width: auto;
  margin-right: 10px;
}

small {
  display: block;
  margin-top: 5px;
  color: #6c757d;
  font-size: 12px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn, .save-btn {
  padding: 10px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-btn {
  background-color: #f8f9fa;
  border: 1px solid #ddd;
  color: #333;
}

.save-btn {
  background-color: #4CAF50;
  border: none;
  color: white;
}

.save-btn:disabled {
  background-color: #9e9e9e;
  cursor: not-allowed;
}

.filters {
  display: flex;
  gap: 10px;
}

.filters select {
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.loading, .error, .no-data {
  text-align: center;
  margin: 40px 0;
  font-size: 18px;
}

.error {
  color: #f44336;
}

.submission-details {
  background-color: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.detail-row {
  margin-bottom: 10px;
}

.detail-row strong {
  margin-right: 5px;
}

.confirmation-message {
  margin-bottom: 20px;
  line-height: 1.5;
}

.confirmation-message p {
  margin-bottom: 10px;
}
</style>
