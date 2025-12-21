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
  <div class="student-home">
    <div class="hero-section">
      <div class="container">
        <div class="hero-content fade-in-up">
          <div class="hero-emoji">🎨✨</div>
          <h1 class="hero-title">Welcome to Spark!</h1>
          <p class="hero-subtitle">
            Show off your amazing Scratch projects and beautiful Canva designs! 
            Pick a category below to get started on your creative journey! 🚀
          </p>
        </div>
      </div>
    </div>

    <div class="categories-section">
      <div class="container">
        <div class="section-header">
          <h2>Choose Your Adventure! 🌟</h2>
          <p>Click on a category to see all the fun projects you can work on</p>
        </div>
        
        <CategoryList 
          @category-selected="handleCategorySelected"
          :loading="loadingWeeks"
        />
      </div>
    </div>
  </div>
</template>

<style scoped>
.student-home {
  display: flex;
  flex-direction: column;
  min-height: auto;
}

.hero-section {
  padding: 3rem 0 2.5rem;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 50%);
  animation: float 6s ease-in-out infinite;
}

.hero-content {
  position: relative;
  z-index: 2;
}

.hero-emoji {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: bounce 2s ease-in-out infinite;
}

.hero-title {
  color: var(--text-white);
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
}

.hero-subtitle {
  color: var(--text-white);
  font-size: 1.3rem;
  font-weight: 400;
  max-width: 600px;
  margin: 0 auto;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
  line-height: 1.6;
}

.categories-section {
  padding: 2.5rem 0 3rem;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  position: relative;
  border-radius: 30px 30px 0 0;
  margin-top: -30px;
}

.section-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.section-header h2 {
  color: var(--text-primary);
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.section-header p {
  color: var(--text-secondary);
  font-size: 1.1rem;
  font-weight: 400;
}

@keyframes float {
  0%, 100% { transform: translateY(0px) rotate(0deg); }
  50% { transform: translateY(-20px) rotate(5deg); }
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.1rem;
    padding: 0 1rem;
  }
  
  .hero-emoji {
    font-size: 3rem;
  }
  
  .section-header h2 {
    font-size: 2rem;
  }
  
  .hero-section {
    padding: 3rem 0;
  }
}
</style>
