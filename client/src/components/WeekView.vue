<template>
  <div class="week-view">
    <div class="header">
      <button class="back-btn" @click="goBack">← Back to Categories</button>
      <h2>{{ categoryInfo.name }}: Week {{ weekNumber }}</h2>
    </div>
    
    <div v-if="loading" class="loading">Loading assignment details...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="assignment-card">
      <h3>{{ weekData.title }}</h3>
      <p class="description">{{ weekData.description }}</p>
      
      <div class="assignment-details">
        <div class="detail">
          <strong>Due Date:</strong> 
          <span>{{ formatDate(weekData.due_date) }}</span>
        </div>
        <div class="detail" v-if="weekData.assignment_url">
          <strong>Assignment Link:</strong>
          <a :href="weekData.assignment_url" target="_blank" rel="noopener noreferrer">
            View Assignment
          </a>
        </div>
      </div>
      
      <div class="submission-section">
        <h4>Your Submission</h4>
        <div v-if="hasSubmitted" class="existing-submission">
          <p>You've already submitted a project for this week:</p>
          <a :href="userSubmission.project_url" target="_blank" rel="noopener noreferrer" class="submission-link">
            {{ userSubmission.project_url }}
          </a>
          <p v-if="userSubmission.comment" class="comment">
            <strong>Your comment:</strong> {{ userSubmission.comment }}
          </p>
          <p class="submitted-date">
            Submitted on {{ formatDate(userSubmission.submitted_at) }}
          </p>
          <button @click="showSubmissionForm = true" class="update-btn">Update Submission</button>
        </div>
        <div v-else>
          <p>You haven't submitted a project for this week yet.</p>
          <button @click="showSubmissionForm = true" class="submit-btn">Submit Your Project</button>
        </div>
      </div>
    </div>
    
    <UploadForm 
      v-if="showSubmissionForm" 
      :category-id="categoryId" 
      :week-number="weekNumber"
      :existing-submission="userSubmission"
      @close="showSubmissionForm = false"
      @submission-complete="handleSubmissionComplete"
    />
  </div>
</template>

<script>
import UploadForm from './UploadForm.vue'

export default {
  name: 'WeekView',
  components: {
    UploadForm
  },
  props: {
    categoryId: {
      type: Number,
      required: true
    },
    weekNumber: {
      type: Number,
      required: true
    },
    categoryInfo: {
      type: Object,
      required: true
    },
    studentId: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      weekData: {},
      loading: true,
      error: null,
      showSubmissionForm: false,
      userSubmission: null
    }
  },
  computed: {
    hasSubmitted() {
      return this.userSubmission !== null
    }
  },
  mounted() {
    this.fetchWeekData()
  },
  methods: {
    async fetchWeekData() {
      try {
        this.loading = true
        const response = await fetch(`http://localhost:5000/api/categories/${this.categoryId}/weeks/${this.weekNumber}?include_submissions=true`)
        if (!response.ok) {
          throw new Error(`Error fetching week data: ${response.statusText}`)
        }
        this.weekData = await response.json()
        
        // Find the user's submission if it exists
        if (this.weekData.submissions) {
          this.userSubmission = this.weekData.submissions.find(
            sub => sub.student_id === this.studentId
          ) || null
        }
        
        this.loading = false
      } catch (err) {
        this.error = err.message
        this.loading = false
        console.error('Failed to fetch week data:', err)
      }
    },
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
    },
    goBack() {
      this.$emit('go-back')
    },
    handleSubmissionComplete(submission) {
      this.userSubmission = submission
      this.showSubmissionForm = false
      this.fetchWeekData() // Refresh data
    }
  }
}
</script>

<style scoped>
.week-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.back-btn {
  background-color: #f8f9fa;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 8px 16px;
  margin-right: 20px;
  cursor: pointer;
}

.assignment-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.description {
  margin: 16px 0;
  line-height: 1.6;
}

.assignment-details {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 16px;
  margin: 20px 0;
}

.detail {
  margin-bottom: 10px;
}

.submission-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #dee2e6;
}

.existing-submission {
  background-color: #e8f4f8;
  border-radius: 6px;
  padding: 16px;
  margin-top: 10px;
}

.submission-link {
  display: block;
  margin: 10px 0;
  word-break: break-all;
  color: #0066cc;
}

.comment {
  font-style: italic;
  margin: 10px 0;
}

.submitted-date {
  font-size: 0.9em;
  color: #6c757d;
  margin-bottom: 15px;
}

.submit-btn, .update-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.update-btn {
  background-color: #17a2b8;
}

.loading, .error {
  text-align: center;
  margin: 40px 0;
  font-size: 18px;
}

.error {
  color: #dc3545;
}
</style>
