<template>
  <div class="upload-form-overlay">
    <div class="upload-form">
      <div class="form-header">
        <h3>Submit Your Canva Project</h3>
        <button class="close-btn" @click="close">×</button>
      </div>
      
      <div v-if="error" class="error-message">{{ error }}</div>
      
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="student-name">Full Name:</label>
          <input 
            id="student-name"
            v-model="formData.student_name"
            type="text" 
            placeholder="Enter your full name"
            required
            :disabled="isSubmitting"
          />
        </div>

        <div class="form-group">
          <label for="project-url">Canva Project URL:</label>
          <input 
            id="project-url"
            v-model="formData.projectUrl"
            type="url" 
            placeholder="https://www.canva.com/design/your-design-id/view"
            required
            :disabled="isSubmitting"
          />
          <small>Please enter the shareable URL of your Canva project</small>
        </div>
        
        <div class="form-group">
          <label for="comment">Comment (optional):</label>
          <textarea 
            id="comment"
            v-model="formData.comment"
            placeholder="Add any comments about your project here..."
            rows="3"
            :disabled="isSubmitting"
          ></textarea>
        </div>
        
        <div class="form-actions">
          <button 
            type="button" 
            class="cancel-btn" 
            @click="close"
            :disabled="isSubmitting"
          >
            Cancel
          </button>
          <button 
            type="submit" 
            class="submit-btn" 
            :disabled="isSubmitting || !isValidUrl"
          >
            <span v-if="isSubmitting">
              <span class="spinner"></span> Submitting...
            </span>
            <span v-else>
              Submit Project
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { api } from '../api'

export default {
  name: 'CanvaUploadForm',
  props: {
    categoryId: {
      type: Number,
      required: true
    },
    weekNumber: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      formData: {
        student_name: '',
        projectUrl: '',
        comment: ''
      },
      isSubmitting: false,
      error: null
    }
  },
  computed: {
    isValidUrl() {
      if (!this.formData.projectUrl) return false
      try {
        const url = new URL(this.formData.projectUrl)
        return url.hostname === 'www.canva.com' && url.pathname.includes('/design/')
      } catch {
        return false
      }
    }
  },
  methods: {
    async submitForm() {
      if (!this.isValidUrl) return

      this.isSubmitting = true
      this.error = null

      const submissionData = {
        student_name: this.formData.student_name,
        project_url: this.formData.projectUrl,
        comment: this.formData.comment || null
      };

      try {
        const submission = await api.submitProject(this.categoryId, this.weekNumber, submissionData)
        this.$emit('submission-complete', submission);
      } catch (err) {
        this.error = err.message;
        console.error('Submission error:', err);
      } finally {
        this.isSubmitting = false;
      }
    },
    close() {
      this.$emit('close')
    }
  }
}
</script>

<style scoped>
.upload-form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.upload-form {
  background-color: white;
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  padding: 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

input, textarea {
  width: 100%;
  padding: 10px;
  border: 1px solid #ced4da;
  border-radius: 4px;
  font-size: 16px;
}

small {
  display: block;
  margin-top: 5px;
  color: #6c757d;
  font-size: 12px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.cancel-btn {
  background-color: #f8f9fa;
  border: 1px solid #ced4da;
  color: #212529;
  padding: 10px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn {
  background-color: #4CAF50;
  color: white;
  border: none;
  padding: 10px 16px;
  border-radius: 4px;
  cursor: pointer;
}

.submit-btn:disabled {
  background-color: #8bc34a;
  cursor: not-allowed;
  opacity: 0.7;
}

.error-message {
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  border-radius: 4px;
  margin-bottom: 16px;
}

.spinner {
  display: inline-block;
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255,255,255,0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s ease-in-out infinite;
  margin-right: 8px;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
