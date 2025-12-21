<template>
  <div class="week-view">
    <!-- Breadcrumb Navigation -->
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <ol class="breadcrumb-list">
        <li><a href="#" @click.prevent="goBack" class="breadcrumb-link">Categories</a></li>
        <li class="breadcrumb-separator">/</li>
        <li><span class="breadcrumb-current">{{ categoryInfo.name }}</span></li>
        <li class="breadcrumb-separator">/</li>
        <li><span class="breadcrumb-current">Week {{ weekNumber }}</span></li>
      </ol>
    </nav>

    <!-- Header Section -->
    <div class="week-header">
      <button 
        class="back-btn" 
        @click="goBack"
        aria-label="Go back to categories"
        :tabindex="0"
      >
        <span class="back-icon" aria-hidden="true">←</span>
        <span>Back to Categories</span>
      </button>
      
      <div class="header-content">
        <div class="category-badge" role="badge">{{ categoryInfo.name }}</div>
        <h1 class="week-title">Week {{ weekNumber }}</h1>
        <p class="week-subtitle">Let's learn something amazing!</p>
      </div>
    </div>
    
    <!-- Loading State with Skeleton -->
    <div v-if="loading" class="loading-state">
      <div class="skeleton-container">
        <div class="skeleton-card">
          <div class="skeleton-badge"></div>
          <div class="skeleton-title"></div>
          <div class="skeleton-text"></div>
          <div class="skeleton-text short"></div>
          <div class="skeleton-grid">
            <div class="skeleton-detail"></div>
            <div class="skeleton-detail"></div>
          </div>
        </div>
        <div class="skeleton-cta"></div>
      </div>
      <p class="loading-text" role="status" aria-live="polite">Loading assignment details...</p>
    </div>
    
    <!-- Error State -->
    <div v-else-if="error" class="error-state" role="alert">
      <div class="error-icon" aria-hidden="true">⚠️</div>
      <h3>Oops! Something went wrong</h3>
      <p>{{ error }}</p>
      <button 
        class="btn-retry" 
        @click="loadWeekData"
        aria-label="Retry loading assignment"
      >
        Try Again
      </button>
    </div>
    
    <!-- Main Content -->
    <div v-else class="week-content" :class="{ 'fade-in': !loading }">
      <!-- Assignment Card -->
      <article class="assignment-card" role="article">
        <div class="card-badge">
          <span class="badge-icon" aria-hidden="true">📚</span>
          <span>Assignment</span>
        </div>
        
        <h2 class="assignment-title">{{ weekData.title || 'Untitled Assignment' }}</h2>
        
        <div class="assignment-body">
          <!-- Metadata Pills -->
          <div class="metadata-pills" v-if="weekData.due_date">
            <div 
              class="pill" 
              :class="getDueDateClass(weekData.due_date)"
              role="status"
            >
              <span class="pill-icon" aria-hidden="true">⏰</span>
              <span>{{ getDueDateText(weekData.due_date) }}</span>
            </div>
            <div class="pill info">
              <span class="pill-icon" aria-hidden="true">📊</span>
              <span>Beginner Friendly</span>
            </div>
            <div class="pill info">
              <span class="pill-icon" aria-hidden="true">⏱️</span>
              <span>~2 hours</span>
            </div>
          </div>

          <!-- Description -->
          <div class="section">
            <div class="section-header">
              <span class="section-icon" aria-hidden="true">✏️</span>
              <h3>What You'll Create</h3>
            </div>
            <p class="description-text">
              {{ weekData.description || 'No description available for this assignment.' }}
            </p>
          </div>
          
          <!-- Details Grid -->
          <div class="details-grid">
            <!-- Due Date -->
            <div class="detail-card" role="group" aria-label="Due date information">
              <div class="detail-icon" aria-hidden="true">📅</div>
              <div class="detail-info">
                <span class="detail-label">Due Date</span>
                <span class="detail-value">{{ formatDate(weekData.due_date) }}</span>
              </div>
            </div>
            
            <!-- Assignment Link -->
            <div 
              v-if="weekData.assignment_url" 
              class="detail-card clickable" 
              @click="openAssignment(weekData.assignment_url)"
              @keydown.enter="openAssignment(weekData.assignment_url)"
              @keydown.space.prevent="openAssignment(weekData.assignment_url)"
              tabindex="0"
              role="button"
              aria-label="Open full assignment instructions"
            >
              <div class="detail-icon" aria-hidden="true">🔗</div>
              <div class="detail-info">
                <span class="detail-label">Instructions</span>
                <span class="detail-value link">View Full Assignment →</span>
              </div>
            </div>

            <!-- Empty State for Missing Link -->
            <div v-else class="detail-card empty">
              <div class="detail-icon" aria-hidden="true">📝</div>
              <div class="detail-info">
                <span class="detail-label">Instructions</span>
                <span class="detail-value muted">Instructions will be available soon</span>
              </div>
            </div>
          </div>
        </div>
      </article>
      
      <!-- Submission Section -->
      <div 
        v-if="!existingSubmission" 
        class="submission-prompt"
        role="region"
        aria-label="Submit your project"
      >
        <div class="prompt-content">
          <div class="prompt-icon animate-pulse" aria-hidden="true">🎯</div>
          <div class="prompt-text">
            <h3>Ready to Submit Your Work?</h3>
            <p>Share your amazing creation with the class!</p>
          </div>
        </div>
        <button 
          class="btn-submit" 
          @click="showSubmissionForm = true"
          aria-label="Open submission form"
        >
          <span class="btn-icon" aria-hidden="true">📤</span>
          <span>Submit Project</span>
        </button>
      </div>
      
      <!-- Existing Submission with Celebration -->
      <div 
        v-else 
        class="submission-card"
        role="region"
        aria-label="Your submission"
        :class="{ 'celebrate': justSubmitted }"
      >
        <div class="submission-header">
          <div class="submission-badge success" role="status">
            <span class="badge-icon" aria-hidden="true">✅</span>
            <span>Submitted</span>
          </div>
          <button 
            class="btn-edit" 
            @click="showSubmissionForm = true"
            aria-label="Edit your submission"
          >
            <span aria-hidden="true">✏️</span>
            <span>Edit Submission</span>
          </button>
        </div>
        
        <div class="submission-body">
          <div class="submission-meta">
            <span class="meta-label">Submitted on</span>
            <time class="meta-value" :datetime="existingSubmission.submitted_at">
              {{ formatDate(existingSubmission.submitted_at) }}
            </time>
          </div>
          
          <div class="submission-details">
            <div class="detail-row">
              <span class="row-label">Student Name</span>
              <span class="row-value">{{ existingSubmission.student_name }}</span>
            </div>
            
            <div class="detail-row">
              <span class="row-label">Project Link</span>
              <a 
                :href="existingSubmission.project_url" 
                target="_blank" 
                rel="noopener noreferrer" 
                class="row-link"
                :aria-label="`Open project link: ${existingSubmission.project_url}`"
              >
                {{ truncateUrl(existingSubmission.project_url) }}
                <span class="link-icon" aria-hidden="true">↗</span>
              </a>
            </div>
            
            <div v-if="existingSubmission.comment" class="detail-row comment-row">
              <span class="row-label">Your Comment</span>
              <p class="row-comment">{{ existingSubmission.comment }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Success Toast -->
      <Transition name="toast">
        <div v-if="showSuccessToast" class="success-toast" role="alert" aria-live="polite">
          <span class="toast-icon" aria-hidden="true">🎉</span>
          <span class="toast-message">Assignment submitted successfully!</span>
        </div>
      </Transition>
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
const showSuccessToast = ref(false)
const justSubmitted = ref(false)

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

const getDueDateText = (dateString) => {
  if (!dateString) return 'No due date'
  const dueDate = new Date(dateString)
  const today = new Date()
  const diffTime = dueDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'Overdue'
  if (diffDays === 0) return 'Due today'
  if (diffDays === 1) return 'Due tomorrow'
  if (diffDays <= 7) return `Due in ${diffDays} days`
  return 'Due soon'
}

const getDueDateClass = (dateString) => {
  if (!dateString) return 'pill'
  const dueDate = new Date(dateString)
  const today = new Date()
  const diffTime = dueDate - today
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays < 0) return 'pill danger'
  if (diffDays <= 3) return 'pill warning'
  return 'pill success'
}

const truncateUrl = (url) => {
  if (!url) return ''
  if (url.length <= 50) return url
  return url.substring(0, 47) + '...'
}

const openAssignment = (url) => {
  window.open(url, '_blank', 'noopener,noreferrer')
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
  
  // Show success animation and toast
  justSubmitted.value = true
  showSuccessToast.value = true
  
  // Hide toast after 3 seconds
  setTimeout(() => {
    showSuccessToast.value = false
  }, 3000)
  
  // Remove celebration class after animation
  setTimeout(() => {
    justSubmitted.value = false
  }, 1000)
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
/* ===== Layout & Container ===== */
.week-view {
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.95) 0%, rgba(118, 75, 162, 0.95) 100%);
  padding: 0;
  position: relative;
}

/* ===== Breadcrumb Navigation ===== */
.breadcrumb {
  background: rgba(255, 255, 255, 0.98);
  padding: 0.75rem 2rem;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.breadcrumb-list {
  display: flex;
  align-items: center;
  list-style: none;
  margin: 0;
  padding: 0;
  font-size: 0.9rem;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.breadcrumb-link {
  color: #6366f1;
  text-decoration: none;
  transition: all 0.2s ease;
  font-weight: 500;
}

.breadcrumb-link:hover {
  color: #4f46e5;
  text-decoration: underline;
}

.breadcrumb-link:focus-visible {
  outline: 2px solid #6366f1;
  outline-offset: 2px;
  border-radius: 4px;
}

.breadcrumb-separator {
  color: #9ca3af;
  margin: 0 0.25rem;
  user-select: none;
}

.breadcrumb-current {
  color: #6b7280;
  font-weight: 600;
}

/* ===== Header Section ===== */
.week-header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 1.5rem 2rem;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
  position: sticky;
  top: 0;
  z-index: 100;
}

.back-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: transparent;
  border: 2px solid #6366f1;
  border-radius: 8px;
  color: #6366f1;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  margin-bottom: 1.5rem;
}

.back-btn:hover {
  background: #6366f1;
  color: white;
  transform: translateX(-4px);
}

.back-btn:focus-visible {
  outline: 3px solid #6366f1;
  outline-offset: 3px;
}

.back-icon {
  font-size: 1.2rem;
  font-weight: bold;
}

.header-content {
  text-align: center;
}

.category-badge {
  display: inline-block;
  padding: 0.4rem 1rem;
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin-bottom: 0.75rem;
}

.week-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0.5rem 0;
  line-height: 1.2;
}

.week-subtitle {
  font-size: 1.1rem;
  color: #6b7280;
  margin: 0;
  font-weight: 400;
}

/* ===== Loading & Error States ===== */
.loading-state,
.error-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  min-height: 400px;
  color: white;
}

/* Skeleton Loader */
.skeleton-container {
  max-width: 900px;
  margin: 0 auto 2rem;
  padding: 0 2rem;
}

.skeleton-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 1.5rem;
}

.skeleton-badge {
  width: 120px;
  height: 24px;
  background: linear-gradient(90deg, #e5e7eb 25%, #f3f4f6 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 4px;
  margin-bottom: 1.5rem;
}

.skeleton-title {
  width: 60%;
  height: 32px;
  background: linear-gradient(90deg, #e5e7eb 25%, #f3f4f6 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 8px;
  margin-bottom: 1.5rem;
}

.skeleton-text {
  width: 100%;
  height: 20px;
  background: linear-gradient(90deg, #e5e7eb 25%, #f3f4f6 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 4px;
  margin-bottom: 1rem;
}

.skeleton-text.short {
  width: 80%;
}

.skeleton-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
}

.skeleton-detail {
  height: 80px;
  background: linear-gradient(90deg, #e5e7eb 25%, #f3f4f6 50%, #e5e7eb 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 12px;
}

.skeleton-cta {
  max-width: 900px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 100px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.3) 25%, rgba(255, 255, 255, 0.5) 50%, rgba(255, 255, 255, 0.3) 75%);
  background-size: 200% 100%;
  animation: skeleton-loading 1.5s ease-in-out infinite;
  border-radius: 16px;
}

@keyframes skeleton-loading {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.loading-text {
  font-size: 1.1rem;
  margin-top: 0.5rem;
  color: white;
  font-weight: 500;
}

.spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top-color: white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 1.5rem;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading-state p,
.error-state p {
  font-size: 1.1rem;
  margin-top: 0.5rem;
}

.error-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.error-state h3 {
  color: white;
  margin-bottom: 0.5rem;
}

.btn-retry {
  margin-top: 1.5rem;
  padding: 0.75rem 1.5rem;
  background: white;
  color: #6366f1;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-retry:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

/* ===== Main Content ===== */
.week-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

/* ===== Assignment Card ===== */
.assignment-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.assignment-card:hover {
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: linear-gradient(135deg, #f3f4f6, #e5e7eb);
  color: #4b5563;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.badge-icon {
  font-size: 1rem;
}

.assignment-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #111827;
  margin: 0;
  padding: 1.5rem 2rem 1rem;
  line-height: 1.3;
}

.assignment-body {
  padding: 0 2rem 2rem;
}

/* ===== Metadata Pills ===== */
.metadata-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.875rem;
  font-weight: 600;
  transition: all 0.2s ease;
}

.pill.success {
  background: #d1fae5;
  color: #065f46;
  border: 1px solid #10b981;
}

.pill.warning {
  background: #fef3c7;
  color: #92400e;
  border: 1px solid #f59e0b;
}

.pill.danger {
  background: #fee2e2;
  color: #991b1b;
  border: 1px solid #ef4444;
}

.pill.info {
  background: #e0e7ff;
  color: #3730a3;
  border: 1px solid #6366f1;
}

.pill-icon {
  font-size: 1rem;
}

/* ===== Animations ===== */
.fade-in {
  animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.animate-pulse {
  animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
  0%, 100% {
    opacity: 1;
    transform: scale(1);
  }
  50% {
    opacity: 0.8;
    transform: scale(1.05);
  }
}

/* Celebration Animation */
.celebrate {
  animation: celebrate 0.6s ease-out;
}

@keyframes celebrate {
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
}

/* ===== Section Styling ===== */
.section {
  margin-bottom: 2rem;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1rem;
}

.section-icon {
  font-size: 1.5rem;
}

.section-header h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin: 0;
}

.description-text {
  font-size: 1.05rem;
  line-height: 1.7;
  color: #4b5563;
  background: #f9fafb;
  padding: 1.25rem;
  border-radius: 12px;
  border-left: 4px solid #6366f1;
  margin: 0;
}

/* ===== Details Grid ===== */
.details-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
  margin-top: 1.5rem;
}

.detail-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1.25rem;
  background: #f9fafb;
  border: 2px solid #e5e7eb;
  border-radius: 12px;
  transition: all 0.2s ease;
}

.detail-card.clickable {
  cursor: pointer;
}

.detail-card.clickable:hover {
  background: #f3f4f6;
  border-color: #6366f1;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.1);
}

.detail-card.clickable:focus-visible {
  outline: 3px solid #6366f1;
  outline-offset: 2px;
}

/* Empty State for Detail Card */
.detail-card.empty {
  opacity: 0.7;
  border-style: dashed;
}

.detail-card.empty .detail-value {
  color: #9ca3af;
  font-style: italic;
}

.detail-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  flex: 1;
}

.detail-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-value {
  font-size: 1rem;
  font-weight: 600;
  color: #111827;
}

.detail-value.link {
  color: #6366f1;
  display: flex;
  align-items: center;
  gap: 0.25rem;
}

/* ===== Submission Prompt ===== */
.submission-prompt {
  background: linear-gradient(135deg, #10b981, #059669);
  border-radius: 16px;
  padding: 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
  box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
  transition: all 0.3s ease;
}

.submission-prompt:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(16, 185, 129, 0.4);
}

.prompt-content {
  display: flex;
  align-items: center;
  gap: 1.5rem;
  flex: 1;
}

.prompt-icon {
  font-size: 3rem;
  flex-shrink: 0;
}

.prompt-text h3 {
  color: white;
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
}

.prompt-text p {
  color: rgba(255, 255, 255, 0.9);
  margin: 0;
  font-size: 1rem;
}

.btn-submit {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: white;
  color: #059669;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
}

.btn-icon {
  font-size: 1.3rem;
}

/* ===== Submission Card ===== */
.submission-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  border: 2px solid #10b981;
}

.submission-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem 2rem;
  background: linear-gradient(135deg, #ecfdf5, #d1fae5);
  border-bottom: 1px solid #a7f3d0;
}

.submission-badge {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.submission-badge.success {
  background: #10b981;
  color: white;
}

.btn-edit {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.6rem 1.2rem;
  background: white;
  border: 2px solid #6b7280;
  border-radius: 8px;
  color: #374151;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-edit:hover {
  background: #f9fafb;
  border-color: #6366f1;
  color: #6366f1;
}

.submission-body {
  padding: 2rem;
}

.submission-meta {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  padding-bottom: 1.5rem;
  border-bottom: 1px solid #e5e7eb;
}

.meta-label {
  font-size: 0.9rem;
  color: #6b7280;
  font-weight: 500;
}

.meta-value {
  font-size: 0.95rem;
  color: #111827;
  font-weight: 600;
}

.submission-details {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.row-label {
  font-size: 0.85rem;
  font-weight: 600;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.row-value {
  font-size: 1rem;
  color: #111827;
  font-weight: 500;
}

.row-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: #6366f1;
  text-decoration: none;
  font-weight: 600;
  transition: all 0.2s ease;
  word-break: break-all;
}

.row-link:hover {
  color: #4f46e5;
  gap: 0.75rem;
}

.link-icon {
  font-size: 1rem;
  transition: transform 0.2s ease;
}

.row-link:hover .link-icon {
  transform: translate(2px, -2px);
}

.comment-row {
  background: #f9fafb;
  padding: 1rem;
  border-radius: 8px;
  border-left: 3px solid #6366f1;
}

.row-comment {
  font-size: 1rem;
  line-height: 1.6;
  color: #4b5563;
  margin: 0;
  font-style: italic;
}

/* ===== Success Toast ===== */
.success-toast {
  position: fixed;
  top: 2rem;
  right: 2rem;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  padding: 1rem 1.5rem;
  border-radius: 12px;
  box-shadow: 0 10px 40px rgba(16, 185, 129, 0.4);
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-weight: 600;
  z-index: 1000;
  animation: slideInRight 0.3s ease-out;
}

.toast-icon {
  font-size: 1.5rem;
  animation: bounce 0.5s ease-in-out;
}

.toast-message {
  font-size: 1rem;
}

/* Toast Transitions */
.toast-enter-active {
  animation: slideInRight 0.3s ease-out;
}

.toast-leave-active {
  animation: slideOutRight 0.3s ease-in;
}

@keyframes slideInRight {
  from {
    transform: translateX(400px);
    opacity: 0;
  }
  to {
    transform: translateX(0);
    opacity: 1;
  }
}

@keyframes slideOutRight {
  from {
    transform: translateX(0);
    opacity: 1;
  }
  to {
    transform: translateX(400px);
    opacity: 0;
  }
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* ===== Focus Visible States (Accessibility) ===== */
*:focus-visible {
  outline: 2px solid #6366f1;
  outline-offset: 2px;
  border-radius: 4px;
}

button:focus-visible,
a:focus-visible {
  outline: 3px solid #6366f1;
  outline-offset: 3px;
}

/* ===== Responsive Design ===== */
@media (max-width: 768px) {
  .breadcrumb {
    padding: 0.5rem 1.25rem;
  }

  .breadcrumb-list {
    font-size: 0.8rem;
  }

  .week-header {
    padding: 1rem 1.25rem;
  }
  
  .back-btn {
    margin-bottom: 1rem;
  }
  
  .week-title {
    font-size: 2rem;
  }
  
  .week-subtitle {
    font-size: 1rem;
  }
  
  .week-content {
    padding: 1.25rem;
  }

  .metadata-pills {
    gap: 0.5rem;
  }

  .pill {
    font-size: 0.8rem;
    padding: 0.4rem 0.8rem;
  }

  .skeleton-container {
    padding: 0 1.25rem;
  }

  .skeleton-grid {
    grid-template-columns: 1fr;
  }
  
  .assignment-title {
    font-size: 1.5rem;
    padding: 1.25rem 1.5rem 0.75rem;
  }
  
  .assignment-body {
    padding: 0 1.5rem 1.5rem;
  }
  
  .description-text {
    font-size: 1rem;
    padding: 1rem;
  }
  
  .details-grid {
    grid-template-columns: 1fr;
  }
  
  .submission-prompt {
    flex-direction: column;
    padding: 1.5rem;
    text-align: center;
  }
  
  .prompt-content {
    flex-direction: column;
    text-align: center;
  }
  
  .prompt-text h3 {
    font-size: 1.25rem;
  }
  
  .btn-submit {
    width: 100%;
    justify-content: center;
  }
  
  .submission-header {
    flex-direction: column;
    gap: 1rem;
    align-items: flex-start;
    padding: 1.25rem 1.5rem;
  }
  
  .submission-body {
    padding: 1.5rem;
  }

  .success-toast {
    top: 1rem;
    right: 1rem;
    left: 1rem;
    padding: 0.875rem 1.25rem;
    font-size: 0.9rem;
  }

  .toast-icon {
    font-size: 1.25rem;
  }
}

/* ===== Animation Utilities ===== */
.week-view * {
  box-sizing: border-box;
}

/* Reduce motion for accessibility */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
</style>
