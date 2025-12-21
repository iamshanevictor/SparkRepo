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
.week-layout { display: flex; gap: 2rem; max-width: 1200px; margin: 0 auto; padding: 2rem; }
.sidebar { flex: 0 0 220px; background: #fff; border-radius: 8px; padding: 1rem; box-shadow: 0 2px 4px rgba(0,0,0,.08); height: fit-content; }
.week-list { list-style: none; margin-top: 1rem; padding: 0; }
.week-list li { padding: 0.6rem 0.8rem; border-radius: 6px; cursor: pointer; margin-bottom: 0.5rem; }
.week-list li.active { background: #4CAF50; color: #fff; }
.content { flex: 1; }
</style>
