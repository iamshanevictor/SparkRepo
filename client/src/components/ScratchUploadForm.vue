<template>
  <div class="upload-form-overlay">
    <div class="upload-form">
      <div class="form-header">
        <h3>Submit Your Scratch Project</h3>
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
            autocomplete="name"
            @blur="normalizeStudentName"
            @input="touched.name = true"
            :aria-invalid="Boolean(nameError)"
            aria-describedby="student-name-help student-name-error"
          />
          <small>Enter first and last name (e.g., "Juan Dela Cruz").</small>
          <div
            v-if="nameError && (touched.name || attemptedSubmit)"
            id="student-name-error"
            class="field-error"
          >
            {{ nameError }}
          </div>
        </div>

        <div class="form-group">
          <label for="project-url">Scratch Project URL:</label>
          <input 
            id="project-url"
            v-model="formData.projectUrl"
            type="url" 
            placeholder="https://scratch.mit.edu/projects/123456"
            required
            :disabled="isSubmitting"
            @input="touched.url = true"
            :aria-invalid="Boolean(urlError)"
            aria-describedby="project-url-help project-url-error"
          />
          <small id="project-url-help">Please enter the full URL to your Scratch project</small>
          <div
            v-if="urlError && (touched.url || attemptedSubmit)"
            id="project-url-error"
            class="field-error"
          >
            {{ urlError }}
          </div>
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
            :disabled="isSubmitting || !isValidUrl || !isValidFullName"
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
  name: 'ScratchUploadForm',
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
      error: null,
      attemptedSubmit: false,
      touched: {
        name: false,
        url: false,
      },
    }
  },
  computed: {
    isValidFullName() {
      const parts = (this.formData.student_name || '')
        .trim()
        .split(/\s+/)
        .filter(Boolean)
      return parts.length >= 2 && parts[0].length > 0 && parts[1].length > 0
    },
    isValidUrl() {
      if (!this.formData.projectUrl) return false
      try {
        const url = new URL(this.formData.projectUrl)
        return url.hostname === 'scratch.mit.edu' && url.pathname.startsWith('/projects/')
      } catch {
        return false
      }
    }
    ,
    nameError() {
      const name = (this.formData.student_name || '').trim()
      if (!name) return 'Name is required.'
      if (!this.isValidFullName) return 'Needs to be full name (first and last name).'
      return ''
    },
    urlError() {
      const url = (this.formData.projectUrl || '').trim()
      if (!url) return 'Project link is required.'
      if (!this.isValidUrl) return 'Needs a valid Scratch link (https://scratch.mit.edu/projects/...).'
      return ''
    }
  },
  methods: {
    normalizeName(input) {
      const raw = (input || '').trim()
      if (!raw) return ''
      const collapsed = raw.replace(/\s+/g, ' ')
      return collapsed
        .split(' ')
        .map((word) => {
          const lower = word.toLowerCase()
          const tokens = lower.split(/([\-'])/)
          return tokens
            .map((t) => {
              if (t === '-' || t === "'") return t
              if (!t) return ''
              return t.charAt(0).toUpperCase() + t.slice(1)
            })
            .join('')
        })
        .join(' ')
    },
    normalizeStudentName() {
      this.formData.student_name = this.normalizeName(this.formData.student_name)
    },
    async submitForm() {
      if (!this.isValidUrl) return

      this.attemptedSubmit = true

      this.normalizeStudentName()
      if (!this.isValidFullName) {
        this.error = 'Please enter your full name (first name and last name).'
        return
      }

      this.isSubmitting = true
      this.error = null

      const submissionData = {
        student_name: this.normalizeName(this.formData.student_name),
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
