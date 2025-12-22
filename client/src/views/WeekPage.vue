<script setup>
import { ref, watch, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useWeeksList, useWeekData } from '../composables/useWeekData'
import { useCategories } from '../composables/useCategories'
import WeekView from '../components/WeekView.vue'

const route = useRoute()
const router = useRouter()
const categoryId = ref(route.params.categoryId)
const weekNumber = ref(Number(route.params.weekNumber))

// Use composables for data loading with caching
const { weeks: weeksList } = useWeeksList(categoryId)
const { weekData, existingSubmission, refresh } = useWeekData(categoryId, weekNumber)
const { categories, loadCategories } = useCategories()

const localSubmissionOverride = ref(null)
const toastMessage = ref('')
let toastTimer = null

// Load categories on mount
onMounted(() => {
  loadCategories()
})

// Find current category info
const categoryInfo = computed(() => 
  categories.value.find(cat => cat.id === categoryId.value)
)

// Extract week numbers for navigation
const weeks = computed(() => weeksList.value.map(w => w.week_number))

watch(() => route.params.weekNumber, (newWeek) => {
  weekNumber.value = Number(newWeek)
})

function goToWeek(week) {
  router.push({ 
    name: 'week', 
    params: { categoryId: categoryId.value, weekNumber: week } 
  })
}

function goHome() {
  router.push('/')
}

const effectiveSubmission = computed(() => localSubmissionOverride.value || existingSubmission.value)

function handleSubmissionSuccess(submission) {
  if (submission) {
    localSubmissionOverride.value = submission
  } else {
    // Fallback to a lightweight marker so the UI updates immediately.
    localSubmissionOverride.value = { id: 'local', submitted_at: new Date().toISOString(), status: 'submitted' }
  }

  toastMessage.value = 'Submitted successfully.'
  if (toastTimer) clearTimeout(toastTimer)
  toastTimer = setTimeout(() => { toastMessage.value = '' }, 3200)

  refresh()
}
</script>

<template>
  <div class="week-page">
    <!-- Purple Gradient Background -->
    <div class="background-gradient"></div>
    
    <!-- Back Button Above Panels -->
    <div class="top-actions">
      <button class="back-btn" @click="goHome" title="Back to categories">
        ← Back
      </button>
    </div>

    <div v-if="toastMessage" class="toast" role="status" aria-live="polite">
      {{ toastMessage }}
    </div>
    
    <!-- Three-Panel Container -->
    <div class="panels-container">
      <!-- Left Panel: Weeks -->
      <div class="panel weeks-panel">
        <div class="panel-header">
          <h3>Weeks</h3>
          <button class="icon-btn">
            <span>📋</span>
          </button>
        </div>
        <div class="panel-content">
          <nav class="weeks-nav">
            <button
              v-for="week in weeks"
              :key="week"
              class="week-btn"
              :class="{ active: week === weekNumber }"
              @click="goToWeek(week)"
            >
              <span class="week-icon">📅</span>
              Week {{ week }}
            </button>
          </nav>
        </div>
      </div>

      <!-- Middle Panel: Week Content -->
      <div class="panel content-panel">
        <div class="panel-header">
          <h3>{{ weekData?.title || `Week ${weekNumber}` }}</h3>
          <div class="header-actions">
            <button class="icon-btn"><span>⚙️</span></button>
            <button class="icon-btn"><span>⋮</span></button>
          </div>
        </div>
        <div class="panel-content">
          <WeekView 
            :category-id="categoryId"
            :week-number="weekNumber"
            :week-data="weekData"
            :existing-submission="effectiveSubmission"
            :category-info="categoryInfo"
            @submitted="handleSubmissionSuccess"
          />
        </div>
      </div>

      <!-- Right Panel: Submission Status -->
      <div class="panel status-panel">
        <div class="panel-header">
          <h3>Submitted</h3>
          <button class="icon-btn">
            <span>📋</span>
          </button>
        </div>
        <div class="panel-content status-content">
          <div v-if="effectiveSubmission" class="status-card submitted">
            <div class="status-icon">✅</div>
            <h4>Great Job! 🎉</h4>
            <p>Your work has been submitted!</p>
          </div>
          <div v-else class="status-card not-submitted">
            <div class="status-icon">📝</div>
            <h4>Not Submitted Yet</h4>
            <p>Complete your work and submit when ready!</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.week-page {
  min-height: calc(100vh - 60px);
  position: relative;
  font-family: 'Fredoka', sans-serif;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

/* Purple Gradient Background - Same as Homepage */
.background-gradient {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: -1;
}

.top-actions {
  position: relative;
  z-index: 1;
  padding: 20px 24px 0 24px;
  display: flex;
  justify-content: flex-start;
}

.toast {
  position: fixed;
  top: 92px;
  right: 24px;
  background: rgba(255, 255, 255, 0.95);
  border: 1px solid #d9ddff;
  border-radius: 12px;
  padding: 12px 14px;
  font-weight: 700;
  color: #2f2f4a;
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
  z-index: 10;
}

.back-btn {
  background: white;
  color: #4a4a6a;
  border: 1px solid #d9ddff;
  border-radius: 12px;
  padding: 10px 16px;
  font-weight: 700;
  font-size: 0.95rem;
  cursor: pointer;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
  transition: all 0.2s ease;
}

.back-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 24px rgba(0, 0, 0, 0.18);
}

/* Three-Panel Container */
.panels-container {
  position: relative;
  z-index: 1;
  display: grid;
  grid-template-columns: 1fr 2fr 1fr;
  gap: 16px;
  padding: 24px;
  box-sizing: border-box;
  flex: 1;
  max-height: calc(100vh - 150px);
  overflow: hidden;
}

/* Panel Base Styles - White/Light like homepage cards */
.panel {
  background: white;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  border-top: 4px solid #667eea;
}

.panel-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border-bottom: 1px solid #e8e8ff;
}

.panel-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 700;
  color: #4a4a6a;
  flex: 1;
  text-align: left;
  margin-left: 8px;
}

.header-actions {
  display: flex;
  gap: 4px;
}

.icon-btn {
  background: transparent;
  border: none;
  color: #667eea;
  cursor: pointer;
  padding: 6px 10px;
  border-radius: 8px;
  font-size: 1.1rem;
  transition: all 0.2s;
}

.icon-btn:hover {
  background: rgba(102, 126, 234, 0.1);
  transform: scale(1.1);
}

.panel-content {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  background: white;
}

/* Weeks Panel */
.weeks-nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.week-btn {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 18px;
  background: #f8f9ff;
  border: 2px solid transparent;
  border-radius: 12px;
  color: #4a4a6a;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  text-align: left;
}

.week-btn:hover {
  background: #f0f4ff;
  border-color: #667eea;
  transform: translateX(4px);
}

.week-btn.active {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-color: transparent;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.week-icon {
  font-size: 1.4rem;
}

/* Content Panel */
.content-panel {
  border-top-color: #764ba2;
}

.content-panel .panel-header h3 {
  text-align: center;
  margin-left: 0;
  color: #4a4a6a;
}

/* Status Panel */
.status-panel {
  border-top-color: #f59e0b;
}

.status-content {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
}

.status-card {
  text-align: center;
  padding: 32px 24px;
  border-radius: 16px;
  background: #f8f9ff;
}

.status-icon {
  font-size: 3.5rem;
  margin-bottom: 16px;
}

.status-card h4 {
  margin: 0 0 12px 0;
  font-size: 1.3rem;
  font-weight: 700;
  color: #4a4a6a;
}

.status-card p {
  margin: 0;
  font-size: 1.05rem;
  color: #7a7a9a;
  line-height: 1.5;
}

.status-card.submitted {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
}

.status-card.submitted h4 {
  color: #065f46;
}

.status-card.not-submitted {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
}

.status-card.not-submitted h4 {
  color: #92400e;
}

/* Submit & Edit Buttons */
.btn-submit {
  margin-top: 20px;
  padding: 14px 28px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.btn-submit:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

.btn-edit {
  margin-top: 16px;
  padding: 12px 24px;
  background: white;
  color: #667eea;
  border: 2px solid #667eea;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-edit:hover {
  background: #667eea;
  color: white;
}

/* Responsive */
@media (max-width: 1100px) {
  .panels-container {
    grid-template-columns: 1fr 2fr 1fr;
    gap: 12px;
    padding: 16px;
  }
}

@media (max-width: 900px) {
  .panels-container {
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr auto;
    gap: 12px;
  }
  
  .weeks-panel,
  .status-panel {
    max-height: 200px;
  }
}
</style>
