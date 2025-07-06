<template>
  <div class="class-list">
    <h2>Select Your Class</h2>
    <div v-if="loading" class="loading">Loading classes...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="class-grid">
      <div 
        v-for="classItem in classes" 
        :key="classItem.id" 
        class="class-card"
        @click="selectClass(classItem)"
      >
        <h3>{{ classItem.name }}</h3>
        <p v-if="classItem.description">{{ classItem.description }}</p>
        <button class="select-btn">Select</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClassList',
  data() {
    return {
      classes: [],
      loading: true,
      error: null
    }
  },
  mounted() {
    this.fetchClasses()
  },
  methods: {
    async fetchClasses() {
      try {
        this.loading = true
        const response = await fetch('http://localhost:5000/api/classes')
        if (!response.ok) {
          throw new Error(`Error fetching classes: ${response.statusText}`)
        }
        this.classes = await response.json()
        this.loading = false
      } catch (err) {
        this.error = err.message
        this.loading = false
        console.error('Failed to fetch classes:', err)
      }
    },
    selectClass(classItem) {
      this.$emit('class-selected', classItem)
    }
  }
}
</script>

<style scoped>
.class-list {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.class-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.class-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
}

.class-card:hover {
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
