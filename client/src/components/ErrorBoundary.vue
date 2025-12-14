<template>
  <div v-if="hasError" class="error-boundary">
    <h3>Something went wrong</h3>
    <p>{{ errorMessage }}</p>
    <button @click="handleRetry" class="retry-btn">Retry</button>
  </div>
  <slot v-else></slot>
</template>

<script>
export default {
  name: 'ErrorBoundary',
  data() {
    return {
      hasError: false,
      errorMessage: ''
    };
  },
  errorCaptured(err, vm, info) {
    this.hasError = true;
    this.errorMessage = err.message || 'An unexpected error occurred';
    console.error('Error in component:', err);
    return false;
  },
  methods: {
    handleRetry() {
      this.hasError = false;
      this.errorMessage = '';
      this.$emit('retry');
    }
  }
};
</script>

<style scoped>
.error-boundary {
  padding: 1.5rem;
  border: 1px solid #ff4444;
  background-color: #ffebee;
  color: #c62828;
  border-radius: 8px;
  margin: 1rem;
  text-align: center;
}

.retry-btn {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  background-color: #1976d2;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.retry-btn:hover {
  background-color: #1565c0;
}
</style>
