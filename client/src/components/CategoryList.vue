<template>
  <div class="category-list">
    <h2>Select a Category</h2>
    <div v-if="loading" class="loading">Loading categories...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="category-grid">
      <div 
        v-for="categoryItem in categories" 
        :key="categoryItem.id" 
        class="category-card"
        @click="selectCategory(categoryItem)"
      >
        <h3>{{ categoryItem.name }}</h3>
        <p v-if="categoryItem.description">{{ categoryItem.description }}</p>
        <button class="select-btn">Select</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'CategoryList',
  data() {
    return {
      categories: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.fetchCategories()
  },
  methods: {
    async fetchCategories() {
      try {
        this.loading = true
        const response = await fetch('http://localhost:5000/api/categories')
        if (!response.ok) {
          throw new Error(`Error fetching categories: ${response.statusText}`)
        }
        this.categories = await response.json()
        this.loading = false
      } catch (err) {
        this.error = err.message
        this.loading = false
        console.error('Failed to fetch categories:', err)
      }
    },
    selectCategory(categoryItem) {
      this.$emit('category-selected', categoryItem)
    }
  }
}
</script>

<style scoped>
.category-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.category-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.category-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
}

.select-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 10px;
}

.loading, .error {
  text-align: center;
  margin: 40px 0;
  font-size: 18px;
}

.error {
  color: #dc3545;
}
</style>
