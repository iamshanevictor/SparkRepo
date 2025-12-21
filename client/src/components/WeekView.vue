<template>
  <div class="week-view">
    <div class="week-header">
      <button class="btn btn-outline back-btn" @click="goBack">
        🏠 Back to Categories
      </button>
      <div class="week-title-section">
        <div class="week-emoji">🎯</div>
        <div>
          <h1 class="week-title">{{ categoryInfo.name }}</h1>
          <h2 class="week-subtitle">Week {{ weekNumber }} Adventure!</h2>
        </div>
      </div>
    </div>
    
    <div v-if="loading" class="loading">
      <div class="loading-spinner">🎨</div>
      <p>Loading your awesome assignment...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>Oops! {{ error }}</p>
    </div>
    
    <div v-else class="assignment-container">
      <div class="assignment-card card">
        <div class="card-header">
          <h3 class="assignment-title">🎆 {{ weekData.title }}</h3>
        </div>
        
        <div class="assignment-content">
          <div class="description-section">
            <h4>📝 What You'll Create:</h4>
            <p class="description">{{ weekData.description }}</p>
          </div>
          
          <div class="assignment-details">
            <div class="detail-item">
              <div class="detail-icon">📅</div>
              <div class="detail-content">
                <strong>Due Date:</strong>
                <span class="due-date">{{ formatDate(weekData.due_date) }}</span>
              </div>
            </div>
            
            <div class="detail-item" v-if="weekData.assignment_url">
              <div class="detail-icon">🔗</div>
              <div class="detail-content">
                <strong>Instructions:</strong>
                <a :href="weekData.assignment_url" target="_blank" rel="noopener noreferrer" class="assignment-link">
                  🚀 View Full Assignment
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="submission-card card">
        <div class="submission-header">
          <div class="submission-icon">🏆</div>
          <div>
            <h4>Ready to Show Your Creation?</h4>
            <p>Upload your amazing project and share it with everyone!</p>
          </div>
        </div>
        
        <button @click="showSubmissionForm = true" class="btn btn-success submit-btn">
          🎆 Submit Your Project
        </button>
      </div>
      
      <!-- Existing submission display -->
      <div v-if="existingSubmission" class="existing-submission-card card">
        <div class="submission-status">
          <div class="status-icon">✅</div>
          <div>
            <h4>Great Job! You've Already Submitted</h4>
            <p class="submitted-date">Submitted on {{ formatDate(existingSubmission.submitted_at) }}</p>
          </div>
        </div>
        
        <div class="submission-details">
          <div class="submission-info">
            <strong>👤 Your Name:</strong> {{ existingSubmission.student_name }}
          </div>
          <div class="submission-info">
            <strong>🔗 Project Link:</strong>
            <a :href="existingSubmission.project_url" target="_blank" rel="noopener noreferrer" class="project-link">
              {{ existingSubmission.project_url }}
            </a>
          </div>
          <div v-if="existingSubmission.comment" class="submission-info">
            <strong>💭 Your Note:</strong>
            <p class="comment">{{ existingSubmission.comment }}</p>
          </div>
        </div>
        
        <button @click="showSubmissionForm = true" class="btn btn-warning update-btn">
          ✨ Update Your Submission
        </button>
      </div>
    </div>

    <!-- Upload Form Modal -->
    <UploadForm
      v-if="showSubmissionForm"
      :categoryId="categoryId"
      :weekNumber="weekNumber"
      :existingSubmission="existingSubmission"
      @close="showSubmissionForm = false"
      @submitted="handleSubmissionSuccess"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import UploadForm from './UploadForm.vue'
import { api } from '../api'

const props = defineProps({
  categoryId: {
    type: String,
    required: true,
  },
  weekNumber: {
    type: Number,
    required: true,
  },
  categoryInfo: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['go-back'])
const router = useRouter()

const weekData = ref({})
const existingSubmission = ref(null)
const loading = ref(true)
const error = ref(null)
const showSubmissionForm = ref(false)

const formatDate = (dateString) => {
  if (!dateString) return 'No due date set'
  try {
    return new Date(dateString).toLocaleDateString('en-US', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
    })
  } catch (e) {
    return dateString
  }
}

const goBack = () => {
  emit('go-back')
}

const loadWeekData = async () => {
  try {
    loading.value = true
    error.value = null
    
    // Get week assignment details
    const weekResponse = await api.getWeek(props.categoryId, props.weekNumber)
    weekData.value = weekResponse
    
    // Check for existing submission
    try {
      const submissions = await api.getWeekSubmissions(weekData.value.id)
      existingSubmission.value = submissions.find(s => s.week_id === weekData.value.id) || null
    } catch (submissionError) {
      console.log('No existing submission found:', submissionError)
    }
    
  } catch (err) {
    console.error('Failed to load week data:', err)
    error.value = err.message || 'Failed to load assignment details'
  } finally {
    loading.value = false
  }
}

const handleSubmissionSuccess = (submission) => {
  existingSubmission.value = submission
  showSubmissionForm.value = false
}

// Watch for prop changes
watch(
  () => [props.categoryId, props.weekNumber],
  () => {
    if (props.categoryId && props.weekNumber) {
      loadWeekData()
    }
  },
  { immediate: true }
)

onMounted(() => {
  loadWeekData()
})
</script>

<style scoped>
.week-view {
  min-height: 100vh;
  background: var(--bg-main);
  padding: 2rem 0;
}

.week-header {
  padding: 0 2rem 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.back-btn {
  align-self: flex-start;
  font-size: 1rem;
}

.week-title-section {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  color: var(--text-white);
  text-align: left;
}

.week-emoji {
  font-size: 4rem;
  animation: bounce 2s ease-in-out infinite;
}

.week-title {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 0.5rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.week-subtitle {
  font-size: 1.8rem;
  font-weight: 500;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
  color: rgba(255, 255, 255, 0.9);
}

.loading {
  text-align: center;
  padding: 4rem;
  color: var(--text-white);
}

.loading-spinner {
  font-size: 4rem;
  animation: spin 2s linear infinite;
  margin-bottom: 1rem;
}

.assignment-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.assignment-card {
  background: var(--bg-card);
  border-radius: var(--radius-large);
  overflow: hidden;
}

.card-header {
  background: linear-gradient(135deg, var(--primary-blue), var(--primary-purple));
  color: var(--text-white);
  padding: 2rem;
  text-align: center;
}

.assignment-title {
  font-size: 2rem;
  font-weight: 600;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

.assignment-content {
  padding: 2rem;
}

.description-section {
  margin-bottom: 2rem;
}

.description-section h4 {
  color: var(--text-primary);
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.description {
  color: var(--text-secondary);
  font-size: 1.1rem;
  line-height: 1.7;
  background: #f8f9ff;
  padding: 1.5rem;
  border-radius: var(--radius-medium);
  border-left: 4px solid var(--primary-blue);
}

.assignment-details {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  background: rgba(74, 144, 226, 0.1);
  border-radius: var(--radius-medium);
}

.detail-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.detail-content {
  flex: 1;
}

.detail-content strong {
  color: var(--text-primary);
  display: block;
  margin-bottom: 0.25rem;
  font-weight: 600;
}

.due-date {
  color: var(--primary-purple);
  font-weight: 500;
}

.assignment-link {
  color: var(--primary-blue);
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s ease;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.assignment-link:hover {
  color: var(--primary-purple);
  transform: translateY(-1px);
}

.submission-card {
  background: linear-gradient(135deg, var(--primary-green), #2ecc71);
  color: var(--text-white);
  text-align: center;
}

.submission-header {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.submission-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.submission-header h4 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

.submission-header p {
  color: rgba(255, 255, 255, 0.9);
  font-size: 1rem;
}

.submit-btn {
  font-size: 1.2rem;
  padding: 1rem 2rem;
  background: rgba(255, 255, 255, 0.2);
  color: var(--text-white);
  border: 2px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(10px);
}

.submit-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-3px);
}

.existing-submission-card {
  background: linear-gradient(135deg, var(--primary-orange), #f39c12);
  color: var(--text-white);
}

.submission-status {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.status-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.submission-status h4 {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

.submitted-date {
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.9rem;
}

.submission-details {
  background: rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-medium);
  padding: 1.5rem;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
}

.submission-info {
  margin-bottom: 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.submission-info strong {
  font-weight: 600;
}

.project-link {
  color: rgba(255, 255, 255, 0.9);
  text-decoration: none;
  word-break: break-all;
  transition: all 0.3s ease;
}

.project-link:hover {
  color: white;
  text-decoration: underline;
}

.comment {
  background: rgba(255, 255, 255, 0.1);
  padding: 1rem;
  border-radius: var(--radius-small);
  font-style: italic;
  margin-top: 0.5rem;
}

.update-btn {
  background: rgba(255, 255, 255, 0.2);
  color: var(--text-white);
  border: 2px solid rgba(255, 255, 255, 0.3);
  font-size: 1.1rem;
  padding: 0.8rem 1.5rem;
}

.update-btn:hover {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.5);
  transform: translateY(-3px);
}

@media (max-width: 768px) {
  .week-header {
    padding: 0 1rem 2rem;
  }
  
  .week-title-section {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .week-emoji {
    font-size: 3rem;
  }
  
  .week-title {
    font-size: 2rem;
  }
  
  .week-subtitle {
    font-size: 1.5rem;
  }
  
  .assignment-container {
    padding: 0 1rem;
  }
  
  .assignment-content {
    padding: 1.5rem;
  }
  
  .card-header {
    padding: 1.5rem;
  }
  
  .assignment-title {
    font-size: 1.5rem;
  }
  
  .submission-header {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .submission-status {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
  
  .detail-item {
    flex-direction: column;
    text-align: center;
    gap: 0.5rem;
  }
}
</style>
