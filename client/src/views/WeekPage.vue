<script setup>
import { onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { api } from '../api'
import WeekView from '../components/WeekView.vue'

const route = useRoute()
const router = useRouter()
const weeks = ref([])
const loading = ref(false)
const categoryId = ref(route.params.categoryId)
const weekNumber = ref(Number(route.params.weekNumber))
const categoryInfo = ref(null)

async function loadCategory() {
  try {
    const categories = await api.getCategories()
    categoryInfo.value = categories.find(c => c.id === categoryId.value) || null
  } catch (e) {
    console.error(e)
  }
}

async function loadWeeks() {
  loading.value = true
  try {
    const ws = await api.getWeeks(categoryId.value)
    weeks.value = ws.sort((a, b) => a.week_number - b.week_number)
    // If weekNumber is not in weeks, redirect to first
    if (!weeks.value.find(w => w.week_number === weekNumber.value) && weeks.value.length) {
      router.replace({ name: 'week', params: { categoryId: categoryId.value, weekNumber: weeks.value[0].week_number } })
    }
  } catch (e) {
    console.error(e)
    alert(e.message || 'Failed to load weeks')
  } finally {
    loading.value = false
  }
}

function goToWeek(num) {
  router.push({ name: 'week', params: { categoryId: categoryId.value, weekNumber: num } })
}

function onGoBack() {
  router.push({ name: 'home' })
}

watch(
  () => route.params,
  async (p) => {
    categoryId.value = p.categoryId
    weekNumber.value = Number(p.weekNumber)
    await Promise.all([loadCategory(), loadWeeks()])
  }
)

onMounted(async () => {
  await Promise.all([loadCategory(), loadWeeks()])
})
</script>

<template>
  <div class="week-layout">
    <aside class="sidebar">
      <h3>Weeks</h3>
      <div v-if="loading" class="loading">Loading...</div>
      <ul v-else class="week-list">
        <li v-for="w in weeks" :key="w.id" :class="{ active: w.week_number === weekNumber }" @click="goToWeek(w.week_number)">
          Week {{ w.week_number }}
        </li>
      </ul>
    </aside>

    <section class="content">
      <WeekView
        v-if="categoryInfo"
        :category-id="categoryId"
        :week-number="weekNumber"
        :category-info="categoryInfo"
        @go-back="onGoBack"
      />
    </section>
  </div>
</template>

<style scoped>
.week-layout {
  display: flex;
  gap: 0;
  max-width: 100%;
  margin: 0;
  padding: 0;
  min-height: 100vh;
}

.sidebar {
  flex: 0 0 240px;
  background: white;
  padding: 2rem 1.5rem;
  box-shadow: 2px 0 10px rgba(0, 0, 0, 0.05);
  height: 100vh;
  position: sticky;
  top: 0;
  overflow-y: auto;
}

.sidebar h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0 0 1.5rem 0;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.loading {
  text-align: center;
  color: #6b7280;
  font-size: 0.9rem;
  padding: 1rem 0;
}

.week-list {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.week-list li {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  color: #4b5563;
  transition: all 0.2s ease;
  border: 2px solid transparent;
}

.week-list li:hover {
  background: #f3f4f6;
  color: #374151;
}

.week-list li.active {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  font-weight: 600;
  border-color: #6366f1;
  box-shadow: 0 2px 8px rgba(99, 102, 241, 0.3);
}

.content {
  flex: 1;
  overflow-y: auto;
}

@media (max-width: 768px) {
  .week-layout {
    flex-direction: column;
  }
  
  .sidebar {
    position: relative;
    height: auto;
    flex: 0 0 auto;
    padding: 1.5rem;
  }
  
  .week-list {
    flex-direction: row;
    overflow-x: auto;
    gap: 0.75rem;
  }
  
  .week-list li {
    white-space: nowrap;
    flex-shrink: 0;
  }
}
</style>
