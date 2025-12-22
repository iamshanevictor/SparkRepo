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
      <div class="content-container">
        <div class="section-header">
          <h3>Weeks Management</h3>
          <button class="add-btn" @click="showAddWeekForm = true">Add New Week</button>
        </div>
        
        <div class="table-wrapper">
          <div v-if="loading.weeks" class="loading">Loading weeks...</div>
          <div v-else-if="error.weeks" class="error">{{ error.weeks }}</div>
          <WeeksTable v-else :weeks="weeks" @edit="editWeek" />
        </div>
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
              <label for="category">Project Type</label>
              <select id="category" v-model="editingWeek.category_id" required>
                <option v-for="cls in classes" :key="cls.id" :value="cls.id">
                  {{ cls.name }}
                </option>
              </select>
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
              <button type="button" class="delete-btn" @click="confirmDeleteWeek">Delete Week</button>
              <div class="action-buttons">
                <button type="button" class="cancel-btn" @click="showEditWeekForm = false">Cancel</button>
                <button type="submit" class="save-btn" :disabled="loading.updateWeek">
                  <span v-if="loading.updateWeek">Saving...</span>
                  <span v-else>Save Changes</span>
                </button>
              </div>
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
              <select id="new-week-number" v-model.number="newWeek.week_number" required>
                <option value="" disabled>Select a week number</option>
                <option v-for="num in 12" :key="num" :value="num" :disabled="!availableWeekNumbers.includes(num)">
                  Week {{ num }}{{ !availableWeekNumbers.includes(num) ? ' (Already used)' : '' }}
                </option>
              </select>
            </div>
            
            <div class="form-group">
              <label for="new-title">Assignment Title</label>
              <input type="text" id="new-title" v-model="newWeek.assignmentTitle" placeholder="e.g., Zombie Shooter" required />
              <small>Full title will be: Week {{ newWeek.week_number }}: {{ newWeek.assignmentTitle }}</small>
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
      <div class="content-container">
        <div class="section-header">
          <h3>Submissions Management</h3>
        </div>

        <div class="filters" role="group" aria-label="Submission filters">
          <div class="filter-field">
            <label class="filter-label" for="filter-class">Class</label>
            <select id="filter-class" class="filter-select" v-model="filters.class_id" @change="handleClassFilterChange">
              <option value="">All Classes</option>
              <option v-for="cls in classes" :key="cls.id" :value="cls.id">
                {{ cls.name }}
              </option>
            </select>
          </div>

          <div class="filter-field">
            <label class="filter-label" for="filter-week">Week</label>
            <select id="filter-week" class="filter-select" v-model="filters.week_id" @change="fetchSubmissions">
              <option value="">All Weeks</option>
              <option v-for="week in filteredWeeksForSubmissions" :key="week.id" :value="week.id">
                Week {{ week.week_number }}: {{ week.display_name || week.title }}
              </option>
            </select>
          </div>

          <div class="filter-field">
            <label class="filter-label" for="filter-status">Status</label>
            <select id="filter-status" class="filter-select" v-model="filters.status" @change="fetchSubmissions">
              <option value="">All Statuses</option>
              <option value="pending">Pending</option>
              <option value="submitted">Submitted</option>
              <option value="approved">Approved</option>
              <option value="rejected">Rejected</option>
            </select>
          </div>
        </div>
        
        <div class="table-wrapper">
          <div v-if="loading.submissions" class="loading">Loading submissions...</div>
          <div v-else-if="error.submissions" class="error">{{ error.submissions }}</div>
          <div v-else-if="submissions.length === 0" class="no-data">
            No submissions found with the current filters.
          </div>
          <SubmissionsTable v-else :submissions="submissions" @review="editSubmission" @delete="confirmDeleteSubmission" />
        </div>
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
                <option value="pending">Pending</option>
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
import { api } from '../api'
import { useAuth } from '../composables/useAuth'
import WeeksTable from './admin/WeeksTable.vue'
import SubmissionsTable from './admin/SubmissionsTable.vue'

export default {
  name: 'AdminDashboard',
  components: { WeeksTable, SubmissionsTable },
  
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
        week_number: '',
        assignmentTitle: '',
        title: '',
        display_name: '',
        description: '',
        assignment_url: '',
        due_date_local: ''
      }
    }
  },
  computed: {
        filteredWeeksForSubmissions() {
          if (!this.filters.class_id) return this.weeks
          return (this.weeks || []).filter(w => w.category_id === this.filters.class_id)
        },
    availableWeekNumbers() {
      // Get all used week numbers across ALL categories (Canva and Scratch share the same weeks)
      const usedNumbers = this.weeks.map(w => w.week_number)
      
      // Return week numbers 1-12 that are not used
      const available = []
      for (let i = 1; i <= 12; i++) {
        if (!usedNumbers.includes(i)) {
          available.push(i)
        }
      }
      return available
    }
  },
  mounted() {
    this.fetchClasses()
    this.fetchWeeks()
    this.fetchSubmissions()
  },
  methods: {
    handleClassFilterChange() {
      // If a week is selected that doesn't belong to the chosen class, clear it.
      if (this.filters.week_id && this.filters.class_id) {
        const selectedWeek = (this.weeks || []).find(w => w.id === this.filters.week_id)
        if (selectedWeek && selectedWeek.category_id !== this.filters.class_id) {
          this.filters.week_id = ''
        }
      }
      this.fetchSubmissions()
    },
    // Authentication
    logout() {
      const { logout } = useAuth()
      logout()
      this.$emit('logout')
    },
    
    // Data fetching
    async fetchClasses() {
      this.loading.classes = true
      this.error.classes = null
      try {
        const data = await api.getCategories()
        this.classes = data
      } catch (err) {
        this.error.classes = err.message
        console.error('Error fetching categories:', err)
      } finally {
        this.loading.classes = false
      }
    },
    
    async fetchWeeks() {
      this.loading.weeks = true
      this.error.weeks = null
      try {
        const weeks = await api.getAdminWeeks()
        this.weeks = weeks
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
        const params = {
          ...(this.filters.class_id ? { class_id: this.filters.class_id } : {}),
          ...(this.filters.week_id ? { week_id: this.filters.week_id } : {}),
          ...(this.filters.status ? { status: this.filters.status } : {}),
        }
        const submissions = await api.getAdminSubmissions(params)
        // Admin submissions are stored with week_id; join against loaded weeks
        // so the UI always shows Week # + title even if the backend doesn't.
        const byWeekId = new Map((this.weeks || []).map(w => [w.id, w]))
        this.submissions = (submissions || []).map((s) => {
          const weekId = s.week_id || s.weekId || s.week
          const week = weekId ? byWeekId.get(weekId) : null
          const weekNumber = s.week_number ?? week?.week_number ?? ''
          const weekTitle = s.week_title ?? week?.display_name ?? week?.title ?? ''
          return {
            ...s,
            week_id: weekId || s.week_id,
            week_number: weekNumber,
            week_title: weekTitle,
          }
        })
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
        const weekData = {
          title: this.editingWeek.title,
          category_id: this.editingWeek.category_id,
          display_name: this.editingWeek.display_name,
          description: this.editingWeek.description,
          assignment_url: this.editingWeek.assignment_url,
          is_active: this.editingWeek.is_active,
        }
        if (this.editingWeek.due_date_local) {
          weekData.due_date = new Date(this.editingWeek.due_date_local).toISOString()
        }
        await api.updateWeek(this.editingWeek.id, weekData)
        await this.fetchWeeks()
        this.showEditWeekForm = false
      } catch (err) {
        console.error('Error updating week:', err)
        alert(`Error: ${err.message}`)
      } finally {
        this.loading.updateWeek = false
      }
    },
    
    confirmDeleteWeek() {
      if (confirm(`Are you sure you want to delete Week ${this.editingWeek.week_number}? This action cannot be undone.`)) {
        this.deleteWeek()
      }
    },
    
    async deleteWeek() {
      this.loading.updateWeek = true
      try {
        await api.deleteWeek(this.editingWeek.id)
        await this.fetchWeeks()
        this.showEditWeekForm = false
        alert('Week deleted successfully')
      } catch (err) {
        console.error('Error deleting week:', err)
        alert(`Error: ${err.message}`)
      } finally {
        this.loading.updateWeek = false
      }
    },
    
    async addWeek() {
      this.loading.addWeek = true
      try {
        const weekData = {
          class_id: this.newWeek.class_id,
          week_number: this.newWeek.week_number,
          title: `Week ${this.newWeek.week_number}: ${this.newWeek.assignmentTitle}`,
          display_name: this.newWeek.display_name,
          description: this.newWeek.description,
          assignment_url: this.newWeek.assignment_url,
          due_date_local: this.newWeek.due_date_local
        }
        if (weekData.due_date_local) {
          weekData.due_date = new Date(weekData.due_date_local).toISOString()
        }
        delete weekData.due_date_local
        await api.createWeek(this.newWeek.class_id, weekData)
        await this.fetchWeeks()
        this.newWeek = {
          class_id: '',
          week_number: '',
          assignmentTitle: '',
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
          admin_comment: this.editingSubmission.admin_comment,
        }
        await api.updateSubmission(this.editingSubmission.id, submissionData)
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
        await api.deleteSubmission(this.deletingSubmission.id)
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
  /* IMPORTANT: don't use 100vh here.
     App.vue already lays out <router-view> + footer in a 100vh shell.
     If this component claims 100vh, the footer is pushed below the fold. */
  flex: 1;
  min-height: 0;
  background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
  font-size: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.admin-header {
  background: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  flex-shrink: 0;
}

.admin-header h2 {
  font-size: 1.75rem;
  font-weight: 600;
  color: #1e3c72;
  margin: 0;
}

.logout-btn {
  background: #dc3545;
  color: white;
  border: none;
  padding: 0.625rem 1.25rem;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  font-size: 0.95rem;
  transition: all 0.2s;
}

.logout-btn:hover {
  background: #c82333;
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(220, 53, 69, 0.3);
}

.admin-tabs {
  background: white;
  display: flex;
  gap: 0.25rem;
  padding: 0 2rem;
  border-bottom: 1px solid #e5e7eb;
  flex-shrink: 0;
}

.tab-btn {
  padding: 0.75rem 1.25rem;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.05rem;
  font-weight: 500;
  border-bottom: 3px solid transparent;
  color: #6b7280;
  transition: all 0.2s;
  position: relative;
}

.tab-btn:hover {
  color: #1e3c72;
  background: #f9fafb;
}

.tab-btn.active {
  border-bottom-color: #1e3c72;
  color: #1e3c72;
  background: #f9fafb;
}

.tab-content {
  padding: 1.25rem;
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  min-height: 0;
}

.content-container {
  background: white;
  border-radius: 12px;
  padding: 1.5rem 1.75rem;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  flex: 1;
  display: flex;
    min-height: 0;
  flex-direction: column;
  border: 1px solid #e5e7eb;
  table-layout: fixed;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid #f3f4f6;
  margin-bottom: 1rem;
}

.section-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #111827;
  flex: 1;
}

.add-btn {
  padding: 0.6rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 700;
  font-size: 0.95rem;
  border: none;
  background: #1e3c72;
  color: #ffffff;
  white-space: nowrap;
}

.add-btn:hover {
  background: #16335f;
}

th, td {
  padding: 0.75rem 1rem;
  text-align: left;
  word-wrap: break-word;
}

/* Proper column distribution across full width */
th:nth-child(1), td:nth-child(1) { width: 8%; }
th:nth-child(2), td:nth-child(2) { width: 12%; }
th:nth-child(3), td:nth-child(3) { width: 32%; }
th:nth-child(4), td:nth-child(4) { width: 30%; }
th:nth-child(5), td:nth-child(5) { width: 10%; }
th:nth-child(6), td:nth-child(6) { width: 8%; text-align: center; }

th {
  background: #f8f9fa;
  font-weight: 600;
  color: #374151;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.05em;
  border-bottom: 2px solid #e5e7eb;
}

td {
  border-bottom: 1px solid #f3f4f6;
  color: #1f2937;
  font-size: 0.9rem;
  line-height: 1.4;
}

tr:last-child td {
  border-bottom: none;
}

tr:hover td {
  background: #f9fafb;
}

.status {
  display: inline-block;
  padding: 0.5rem 1rem;
  border-radius: 9999px;
  font-size: 0.9rem;
  font-weight: 600;
  text-transform: capitalize;
}

.status.active {
  background: #d1fae5;
  color: #065f46;
}

.status.inactive {
  background: #f3f4f6;
  color: #6b7280;
}

.status.submitted {
  background: #dbeafe;
  color: #1e40af;
}

.status.approved {
  background: #d1fae5;
  color: #065f46;
}

.status.rejected {
  background: #fee2e2;
  color: #991b1b;
}

.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(17, 24, 39, 0.7);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  animation: fadeIn 0.2s ease-out;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.modal-content {
  background: white;
  border-radius: 12px;
  width: 90%;
  max-width: 650px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 2rem;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  animation: slideUp 0.3s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.75rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #f3f4f6;
}

.modal-header h3 {
  font-size: 1.625rem;
  font-weight: 600;
  color: #111827;
  margin: 0;
}

.close-btn {
  background: #f3f4f6;
  border: none;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  font-size: 1.5rem;
  cursor: pointer;
  color: #6b7280;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.close-btn:hover {
  background: #e5e7eb;
  color: #374151;
}

.form-group {
  margin-bottom: 1.5rem;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 600;
  color: #374151;
  font-size: 1rem;
}

input, select, textarea {
  width: 100%;
  padding: 0.875rem 1.125rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
  font-family: inherit;
}

input:focus, select:focus, textarea:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

textarea {
  resize: vertical;
}

.checkbox-label {
  display: flex;
  align-items: center;
  cursor: pointer;
}

.checkbox-label input {
  width: auto;
  margin-right: 0.625rem;
  cursor: pointer;
}

small {
  display: block;
  margin-top: 0.375rem;
  color: #6b7280;
  font-size: 0.813rem;
}

.form-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
  padding-top: 1.5rem;
  border-top: 2px solid #f3f4f6;
}

.action-buttons {
  display: flex;
  gap: 0.75rem;
}

.cancel-btn, .save-btn {
  padding: 0.875rem 1.75rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 1.05rem;
  transition: all 0.2s;
}

.cancel-btn {
  background: #f3f4f6;
  border: 2px solid #e5e7eb;
  color: #374151;
}

.cancel-btn:hover {
  background: #e5e7eb;
}

.save-btn {
  background: #3b82f6;
  border: none;
  color: white;
}

.save-btn:hover {
  background: #2563eb;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
}

.save-btn:disabled {
  background: #9ca3af;
  cursor: not-allowed;
  transform: none;
}

.delete-btn {
  padding: 0.875rem 1.75rem;
  border-radius: 8px;
  background: #ef4444;
  border: none;
  color: white;
  cursor: pointer;
  font-weight: 600;
  font-size: 1.05rem;
  transition: all 0.2s;
}

.delete-btn:hover {
  background: #dc2626;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}

.filters {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 1rem;
  width: 100%;
  margin-bottom: 0.25rem;
}

.filter-field {
  min-width: 0;
}

.filter-label {
  display: block;
  margin-bottom: 0.35rem;
  font-weight: 700;
  color: #374151;
  font-size: 0.9rem;
}

.filter-select {
  width: 100%;
  padding: 0.85rem 1rem;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  color: #111827;
  font-weight: 600;
  background: #ffffff;
}

.filter-select:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.12);
}

@media (max-width: 980px) {
  .filters {
    grid-template-columns: 1fr;
  }
}

.loading, .error, .no-data {
  text-align: center;
  margin: 2rem 0;
  font-size: 1.125rem;
  font-weight: 500;
  color: #6b7280;
}

.error {
  color: #dc2626;
  background: #fee2e2;
  padding: 1.5rem;
  border-radius: 8px;
  border: 2px solid #fecaca;
}

.submission-details {
  background: #f9fafb;
  padding: 1.25rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  border: 2px solid #e5e7eb;
}

.detail-row {
  margin-bottom: 0.75rem;
  line-height: 1.6;
}

.detail-row strong {
  margin-right: 0.5rem;
  color: #374151;
  font-weight: 600;
}

.confirmation-message {
  margin-bottom: 1.5rem;
  line-height: 1.7;
  color: #4b5563;
}

.confirmation-message p {
  margin-bottom: 0.75rem;
}
</style>
