<template>
  <div class="submission-form-container">
    <h2>Submit Your Project</h2>
    <form @submit.prevent="submitProject">
      <div class="form-group">
        <label for="name">Your Name:</label>
        <input type="text" id="name" v-model="name" required>
      </div>
      <div class="form-group">
        <label for="projectLink">Project Link:</label>
        <input type="url" id="projectLink" v-model="projectLink" required>
      </div>
      <button type="submit">Submit</button>
    </form>
  </div>
</template>

<script>
import { apiPost } from '../services/apiClient'
export default {
  name: 'SubmissionForm',
  data() {
    return {
      name: '',
      projectLink: ''
    };
  },
  methods: {
    async submitProject() {
      try {
        const result = await apiPost('/api/project-submissions', {
          name: this.name,
          project_link: this.projectLink,
        })
        console.log('Submission successful:', result);
        alert('Project submitted successfully!');

        // Clear form
        this.name = '';
        this.projectLink = '';

        // Optionally, emit an event to notify the parent component
        this.$emit('project-submitted', result);

      } catch (error) {
        console.error('Error submitting project:', error);
        alert('Failed to submit project. Please try again.');
      }
    }
  }
};
</script>

<style scoped>
.submission-form-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  background-color: #f9f9f9;
}
h2 {
  text-align: center;
  margin-bottom: 1.5rem;
}
.form-group {
  margin-bottom: 1rem;
}
.form-group label {
  display: block;
  margin-bottom: 0.5rem;
}
.form-group input {
  width: 100%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
}
button {
  display: block;
  width: 100%;
  padding: 0.75rem;
  background-color: #42b983;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}
button:hover {
  background-color: #36a476;
}
</style>
