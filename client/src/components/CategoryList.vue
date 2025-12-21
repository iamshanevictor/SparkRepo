<template>
  <div class="category-list">
    <div v-if="categoriesLoading" class="loading">
      <div class="loading-spinner">🎨</div>
      <p>Loading your creative options...</p>
    </div>
    
    <div v-else-if="error" class="error">
      <p>Oops! Something went wrong: {{ error }}</p>
    </div>
    
    <div v-else class="category-grid">
      <div 
        v-for="(categoryItem, index) in categories" 
        :key="categoryItem.id" 
        :class="['category-card', `card-color-${index % 4}`]"
        @click="selectCategory(categoryItem)"
      >
        <div class="category-icon">
          {{ getCategoryEmoji(categoryItem.name) }}
        </div>
        <div class="category-content">
          <h3 class="category-title">{{ categoryItem.name }}</h3>
          <p v-if="categoryItem.description" class="category-description">
            {{ categoryItem.description }}
          </p>
          <button class="btn btn-primary category-btn" :disabled="props.loading">
            <span v-if="props.loading">
              🎯 Loading...
            </span>
            <span v-else>
              🚀 Start Creating!
            </span>
          </button>
        </div>
        <div class="card-sparkle">✨</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useCategories } from '../composables/useCategories'

const props = defineProps({
  loading: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['category-selected'])

const { categories, loading: categoriesLoading, error, loadCategories } = useCategories()

const getCategoryEmoji = (categoryName) => {
  const name = categoryName.toLowerCase()
  if (name.includes('scratch')) return '🐱'
  if (name.includes('canva')) return '🎨'
  if (name.includes('design')) return '✨'
  if (name.includes('code')) return '💻'
  return '🎯'
}

const selectCategory = (categoryItem) => {
  emit('category-selected', categoryItem)
}

onMounted(() => {
  loadCategories()
})
</script>

<style scoped>
.category-list {
  width: 100%;
}

.loading {
  text-align: center;
  padding: 3rem;
  color: var(--text-white);
}

.loading-spinner {
  font-size: 4rem;
  animation: spin 2s linear infinite;
  margin-bottom: 1rem;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  padding: 0 1rem;
}

.category-card {
  background: var(--bg-card);
  border-radius: var(--radius-large);
  padding: 2rem;
  position: relative;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: var(--shadow-card);
  overflow: hidden;
  min-height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

.category-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  border-radius: var(--radius-large) var(--radius-large) 0 0;
  transition: all 0.3s ease;
}

.card-color-0::before {
  background: linear-gradient(90deg, var(--primary-blue), var(--primary-purple));
}

.card-color-1::before {
  background: linear-gradient(90deg, var(--primary-orange), var(--primary-yellow));
}

.card-color-2::before {
  background: linear-gradient(90deg, var(--primary-pink), var(--primary-purple));
}

.card-color-3::before {
  background: linear-gradient(90deg, var(--primary-green), var(--primary-blue));
}

.category-card:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

.category-card:hover::before {
  height: 100%;
  opacity: 0.1;
}

.category-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
  animation: float 3s ease-in-out infinite;
}

.category-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.category-title {
  color: var(--text-primary);
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.category-description {
  color: var(--text-secondary);
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 1.5rem;
  max-width: 250px;
}

.category-btn {
  font-size: 1rem;
  padding: 0.8rem 1.5rem;
  transition: all 0.3s ease;
}

.category-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
  transform: none;
}

.card-sparkle {
  position: absolute;
  top: 1rem;
  right: 1rem;
  font-size: 1.5rem;
  opacity: 0.6;
  animation: twinkle 2s ease-in-out infinite;
}

@keyframes float {
  0%, 100% { 
    transform: translateY(0px);
  }
  50% { 
    transform: translateY(-10px);
  }
}

@keyframes twinkle {
  0%, 100% { 
    opacity: 0.6;
    transform: scale(1);
  }
  50% { 
    opacity: 1;
    transform: scale(1.2);
  }
}

@media (max-width: 768px) {
  .category-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
    padding: 0 0.5rem;
  }
  
  .category-card {
    padding: 1.5rem;
    min-height: 180px;
  }
  
  .category-icon {
    font-size: 3rem;
  }
  
  .category-title {
    font-size: 1.5rem;
  }
  
  .category-description {
    font-size: 0.9rem;
  }
}
</style>
