<template>
  <div class="week-view">
    <div class="header">
      <button class="back-btn" @click="goBack">← Back to Categories</button>
      <h2>{{ categoryInfo.name }}: Week {{ weekNumber }}</h2>
    </div>
    
    <div v-if="loading" class="loading">Loading assignment details...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="assignment-card">
      <h3>{{ weekData.title }}</h3>
      <p class="description">{{ weekData.description }}</p>
      
      <div class="assignment-details">
        <div class="detail">
          <strong>Due Date:</strong> 
          <span>{{ formatDate(weekData.due_date) }}</span>
        </div>
        <div class="detail" v-if="weekData.assignment_url">
          <strong>Assignment Link:</strong>
          <a :href="weekData.assignment_url" target="_blank" rel="noopener noreferrer">
            View Assignment
          </a>
        </div>
      </div>
      
      <div class="submission-section">
        <h4>Ready to Submit?</h4>
        <p>Click the button below to upload your project for this week.</p>
        <button @click="showSubmissionForm = true" class="submit-btn">Submit Your Project</button>
      </div>
    </div>
    
    <UploadForm
      v-if="showSubmissionForm"
      :category-id="categoryId"
      :week-number="weekNumber"
      :category-info="categoryInfo"
      @close="showSubmissionForm = false"
      @submission-complete="handleSubmissionComplete"
    />
  </div>
</template>

<script>
import { api } from '../api';
import UploadForm from './UploadForm.vue';

export default {
  name: 'WeekView',
  components: {
    UploadForm,
  },
  props: {
    categoryId: {
      type: Number,
      required: true
    },
    weekNumber: {
      type: Number,
      required: false
    },
    categoryInfo: {
      type: Object,
      required: true
    },
  },
  data() {
    return {
      weekData: {},
      loading: true,
      error: null,
      showSubmissionForm: false,
    }
  },
  computed: {},
  watch: {
    weekNumber: {
      immediate: true,
      handler(newWeek) {
        if (newWeek !== null && newWeek !== undefined) {
          this.fetchWeekData();
        }
      }
    }
  },
  methods: {
    async fetchWeekData() {
      try {
        this.loading = true;
        this.error = null;
        this.weekData = await api.getWeek(this.categoryId, this.weekNumber);
      } catch (error) {
        console.error('Error fetching week data:', error);
        this.error = error.message || 'Failed to load week data. Please try again.';
      } finally {
        this.loading = false;
      }
    },
    formatDate(dateString) {
      if (!dateString) return 'N/A'
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    goBack() {
      this.$emit('go-back')
    },
    handleSubmissionComplete(submission) {
      this.showSubmissionForm = false
      // Optionally, show a success message
      alert('Your project has been submitted successfully!')
      this.goBack()
    }
  }
}
</script>

<style scoped>
.week-view {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.back-btn {
  background-color: #000000;
  border: 1px solid #dee2e6;
  border-radius: 4px;
  padding: 8px 16px;
  margin-right: 20px;
  cursor: pointer;
}

.assignment-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 24px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.description {
  margin: 16px 0;
  line-height: 1.6;
}

.assignment-details {
  background-color: #f8f9fa;
  border-radius: 6px;
  padding: 16px;
  margin: 20px 0;
}

.detail {
  margin-bottom: 10px;
}

.submission-section {
  margin-top: 30px;
  padding-top: 20px;
  border-top: 1px solid #dee2e6;
}

.existing-submission {
  background-color: #e8f4f8;
  border-radius: 6px;
  padding: 16px;
  margin-top: 10px;
}

.submission-link {
  display: block;
  margin: 10px 0;
  word-break: break-all;
  color: #0066cc;
}

.comment {
  font-style: italic;
  margin: 10px 0;
}

.submitted-date {
  font-size: 0.9em;
  color: #6c757d;
  margin-bottom: 15px;
}

.submit-btn, .update-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 16px;
}

.update-btn {
  background-color: #17a2b8;
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
