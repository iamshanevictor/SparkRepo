<script setup>
import { ref, computed, watch, toRef } from 'vue'
import UploadForm from './UploadForm.vue'

const props = defineProps({
  categoryId: String,
  weekNumber: [String, Number],
  weekData: Object,
  existingSubmission: Object
})

const emit = defineEmits(['submitted'])

const showSubmissionForm = ref(false)

// Use props directly or fallback to loading state
const loading = computed(() => !props.weekData)

// Compute if due soon (within 7 days)
const isDueSoon = computed(() => {
  if (!props.weekData?.due_date) return false
  const dueDate = new Date(props.weekData.due_date)
  const now = new Date()
  const diffDays = (dueDate - now) / (1000 * 60 * 60 * 24)
  return diffDays <= 7 && diffDays >= 0
})

const isOverdue = computed(() => {
  if (!props.weekData?.due_date) return false
  return new Date(props.weekData.due_date) < new Date()
})

function formatDate(dateStr) {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function handleSubmissionSuccess() {
  showSubmissionForm.value = false
  emit('submitted')
}
</script>

<template>
  <div class="week-view">
    <!-- Loading -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading... ✨</p>
    </div>

    <!-- Error -->
    <div v-else-if="!weekData" class="error">
      <span class="error-icon">😢</span>
      <p>No data available</p>
    </div>

    <!-- Content -->
    <div v-else-if="weekData" class="content">
      <!-- Assignment Badge -->
      <div class="assignment-badge">
        <span class="badge-icon">📚</span>
        <span>ASSIGNMENT</span>
      </div>

      <!-- Title -->
      <h2 class="assignment-title">{{ weekData.title }}</h2>

      <!-- Status Pills -->
      <div class="pills">
        <span v-if="isDueSoon" class="pill due-soon">
          <span>🎯</span> Due Soon
        </span>
        <span v-if="isOverdue" class="pill overdue">
          <span>⚠️</span> Overdue
        </span>
        <span class="pill difficulty">
          <span>📊</span> {{ weekData.difficulty || 'Beginner Friendly' }}
        </span>
        <span class="pill duration">
          <span>⏱️</span> {{ weekData.duration || '~2 hours' }}
        </span>
      </div>

      <!-- What You'll Create -->
      <div class="section">
        <h3 class="section-title">
          <span>✏️</span> What You'll Create
        </h3>
        <div class="section-content">
          <p>{{ weekData?.description || `Activities for Week ${weekNumber}: ${weekData?.title}` }}</p>
        </div>
      </div>

      <!-- Info Cards -->
      <div class="info-cards">
        <div class="info-card">
          <div class="info-icon">📅</div>
          <div class="info-content">
            <span class="info-label">DUE DATE</span>
            <span class="info-value">{{ formatDate(weekData?.due_date) || 'No due date' }}</span>
          </div>
        </div>
        <div class="info-card">
          <div class="info-icon">🔗</div>
          <div class="info-content">
            <span class="info-label">INSTRUCTIONS</span>
            <a v-if="weekData?.instructions_url" :href="weekData.instructions_url" target="_blank" class="info-link">
              View Full Assignment →
            </a>
            <span v-else class="info-value">No instructions yet</span>
          </div>
        </div>
      </div>

      <!-- Submit Section -->
      <div class="submit-section" :class="{ submitted: existingSubmission }">
        <div class="submit-content">
          <span class="submit-icon">{{ existingSubmission ? '✅' : '🎯' }}</span>
          <div class="submit-text">
            <h3>{{ existingSubmission ? 'Great Job! 🎉' : 'Ready to Submit Your Work?' }}</h3>
            <p>{{ existingSubmission ? 'Your work has been submitted!' : 'Share your amazing creation with the class!' }}</p>
          </div>
        </div>
        <button 
          class="submit-btn" 
          :class="{ edit: existingSubmission }"
          @click="showSubmissionForm = true"
        >
          {{ existingSubmission ? '✏️ Edit Submission' : '🚀 Submit Project' }}
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty">
      <span class="empty-icon">📭</span>
      <p>No content yet!</p>
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

<style scoped>
.week-view {
  height: 100%;
  color: #4a4a6a;
  display: flex;
  flex-direction: column;
}

.loading,
.error,
.empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 24px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 4px solid #e8e8ff;
  border-top-color: #667eea;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 16px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.loading p,
.empty p {
  color: #7a7a9a;
  font-size: 1.15rem;
  font-weight: 500;
}

.error-icon,
.empty-icon {
  font-size: 3rem;
  margin-bottom: 12px;
}

.error p {
  color: #ef4444;
  font-weight: 500;
}

/* Content */
.content {
  padding: 8px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

/* Assignment Badge */
.assignment-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 14px;
  background: #f0f4ff;
  border-radius: 8px;
  font-size: 0.85rem;
  font-weight: 700;
  color: #667eea;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  width: fit-content;
}

.badge-icon {
  font-size: 1rem;
}

/* Title */
.assignment-title {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d2d4a;
}

/* Pills */
.pills {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  border: 2px solid;
}

.pill.due-soon {
  background: #fef3c7;
  color: #92400e;
  border-color: #f59e0b;
}

.pill.overdue {
  background: #fee2e2;
  color: #991b1b;
  border-color: #ef4444;
}

.pill.difficulty {
  background: #e0f2fe;
  color: #0369a1;
  border-color: #0ea5e9;
}

.pill.duration {
  background: #f3e8ff;
  color: #7c3aed;
  border-color: #a78bfa;
}

/* Sections */
.section {
  background: #f8f9ff;
  border-radius: 12px;
  padding: 16px;
  border-left: 4px solid #667eea;
}

.section-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin: 0 0 12px 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: #4a4a6a;
}

.section-content p {
  margin: 0;
  color: #6a6a8a;
  line-height: 1.6;
  font-size: 1rem;
}

/* Info Cards */
.info-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.info-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  background: #f8f9ff;
  border-radius: 12px;
  border: 1px solid #e8e8ff;
}

.info-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.info-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.info-label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #9a9aba;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.info-value {
  font-size: 1rem;
  font-weight: 600;
  color: #4a4a6a;
}

.info-link {
  font-size: 1rem;
  font-weight: 600;
  color: #667eea;
  text-decoration: none;
  transition: color 0.2s;
}

.info-link:hover {
  color: #764ba2;
}

/* Submit Section */
.submit-section {
  margin-top: auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  padding: 20px 24px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 16px;
  color: white;
}

.submit-section.submitted {
  background: linear-gradient(135deg, #10b981, #059669);
}

.submit-content {
  display: flex;
  align-items: center;
  gap: 16px;
}

.submit-icon {
  font-size: 2.5rem;
}

.submit-text h3 {
  margin: 0 0 4px 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: white;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.submit-text p {
  margin: 0;
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.95);
  text-shadow: 0 1px 2px rgba(0, 0, 0, 0.2);
}

.submit-btn {
  padding: 14px 28px;
  background: white;
  color: #667eea;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  white-space: nowrap;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.submit-btn.edit {
  color: #059669;
}

/* Responsive */
@media (max-width: 768px) {
  .info-cards {
    grid-template-columns: 1fr;
  }
  
  .submit-section {
    flex-direction: column;
    text-align: center;
  }
  
  .submit-content {
    flex-direction: column;
  }
}
</style>
