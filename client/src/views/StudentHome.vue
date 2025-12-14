<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import CategoryList from '../components/CategoryList.vue'

const router = useRouter()
const categoryWeeks = ref([])
const loadingWeeks = ref(false)

async function handleCategorySelected(category) {
  loadingWeeks.value = true
  try {
    const weeks = await api.getWeeks(category.id)
    const sorted = weeks.sort((a, b) => a.week_number - b.week_number)
    categoryWeeks.value = sorted
    if (sorted.length > 0) {
      router.push({
        name: 'week',
        params: { categoryId: category.id, weekNumber: sorted[0].week_number },
      })
    }
  } catch (e) {
    console.error('Failed to load weeks', e)
    alert(e.message || 'Failed to load weeks')
  } finally {
    loadingWeeks.value = false
  }
}
</script>

<template>
  <div>
    <header class="header">
      <div class="logo-container">
        <img src="/vite.svg" class="logo" alt="SparkRepo" />
        <h1>SparkRepo</h1>
      </div>
      <p class="tagline">Upload and share your Scratch projects</p>
    </header>

    <main class="main">
      <CategoryList @category-selected="handleCategorySelected" />
      <div v-if="loadingWeeks" class="loading">Loading weeks...</div>
    </main>
  </div>
</template>

<style scoped>
.header { background: #fff; padding: 1rem 2rem; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
.logo-container { display: flex; align-items: center; gap: 0.75rem; }
.logo { height: 32px; }
.tagline { color: #666; }
.main { padding: 2rem; }
.loading { margin-top: 1rem; color: #555; }
</style>
