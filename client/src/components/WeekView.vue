<script setup>
import { ref, onMounted, watch } from 'vue'
import { api } from '../api'

const props = defineProps({
  categoryId: String,
  weekNumber: [String, Number]
})

const loading = ref(true)
const error = ref(null)
const weekData = ref(null)

async function loadWeek() {
  loading.value = true
  error.value = null
  try {
    const data = await api.getWeek(props.categoryId, props.weekNumber)
    weekData.value = data
  } catch (e) {
    error.value = e.message || 'Failed to load week'
  } finally {
    loading.value = false
  }
}

watch(() => props.weekNumber, loadWeek)

onMounted(loadWeek)
</script>

<template>
  <div class="week-content">
    <!-- Loading -->
    <div v-if="loading" class="loading">
      <div class="spinner"></div>
      <p>Loading... ✨</p>
    </div>

    <!-- Error -->
    <div v-else-if="error" class="error">
      <span class="error-icon">😢</span>
      <p>{{ error }}</p>
    </div>

    <!-- Content -->
    <div v-else-if="weekData" class="assignment-content">
      <div class="assignment-description">
        <p>{{ weekData.description || 'No description available.' }}</p>
      </div>
      
      <div v-if="weekData.due_date" class="due-date">
        <span class="icon">📅</span>
        <span>Due: {{ new Date(weekData.due_date).toLocaleDateString() }}</span>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else class="empty">
      <span class="empty-icon">📭</span>
      <p>No content yet!</p>
    </div>
  </div>
</template>

<style scoped>
.week-content {
  height: 100%;
  color: #4a4a6a;
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

.assignment-content {
  padding: 8px;
}

.assignment-description {
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  border-left: 4px solid #667eea;
}

.assignment-description p {
  margin: 0;
  line-height: 1.7;
  color: #4a4a6a;
  font-size: 1.1rem;
}

.due-date {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  border-radius: 12px;
  color: #92400e;
  font-size: 1.15rem;
  font-weight: 600;
  border: 2px solid #f59e0b;
}

.due-date .icon {
  font-size: 1.5rem;
}
</style>
