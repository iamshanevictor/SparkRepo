<template>
  <div class="student-identifier-container">
    <div class="student-identifier-box">
      <h2>Welcome to SparkRepo</h2>
      <p>Please enter your full name to continue</p>
      <form @submit.prevent="identifyStudent">
        <div class="form-group">
          <label for="full-name">Full Name:</label>
          <input
            id="full-name"
            v-model="fullName"
            type="text"
            placeholder="Enter your full name"
            required
            :disabled="isSubmitting"
          />
        </div>
        <button type="submit" class="submit-btn" :disabled="isSubmitting">
          {{ isSubmitting ? 'Loading...' : 'Continue' }}
        </button>
        <div v-if="error" class="error-message">{{ error }}</div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'StudentIdentifier',
  data() {
    return {
      fullName: '',
      isSubmitting: false,
      error: null,
    };
  },
  methods: {
    async identifyStudent() {
      if (!this.fullName.trim()) {
        this.error = 'Please enter your name.';
        return;
      }
      this.isSubmitting = true;
      this.error = null;
      try {
        // This endpoint finds a student by name or creates a new one
        const response = await fetch('http://localhost:5000/api/students', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ full_name: this.fullName.trim() }),
        });
        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Failed to identify student.');
        }
        const student = await response.json();
        this.$emit('student-identified', student);
      } catch (err) {
        this.error = err.message;
        console.error('Student identification error:', err);
      } finally {
        this.isSubmitting = false;
      }
    },
  },
};
</script>

<style scoped>
.student-identifier-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: calc(100vh - 200px); /* Adjust based on header/footer height */
  padding: 2rem;
}

.student-identifier-box {
  background: white;
  padding: 2rem 3rem;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 400px;
  width: 100%;
}

h2 {
  margin-bottom: 0.5rem;
  color: #333;
}

p {
  margin-bottom: 1.5rem;
  color: #666;
}

.form-group {
  margin-bottom: 1.5rem;
  text-align: left;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border-color);
  border-radius: 4px;
  font-size: 1rem;
}

.submit-btn {
  width: 100%;
  padding: 0.75rem;
  background-color: var(--primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.submit-btn:disabled {
  background-color: #a5d6a7;
  cursor: not-allowed;
}

.submit-btn:not(:disabled):hover {
  background-color: #45a049;
}

.error-message {
  margin-top: 1rem;
  color: #d32f2f; /* A reddish color for errors */
  font-weight: bold;
}
</style>
