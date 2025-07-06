<template>
  <div class="upload-form-overlay">
    <div class="upload-form">
      <div class="form-header">
        <h3>{{ isUpdate ? 'Update Your Submission' : 'Submit Your Project' }}</h3>
        <button class="close-btn" @click="close">×</button>
      </div>
      
      <div v-if="error" class="error-message">{{ error }}</div>
      
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="project-type">Project Type:</label>
          <select id="project-type" v-model="formData.projectType" :disabled="isSubmitting">
            <option value="scratch">Scratch Project</option>
            <option value="canva">Canva Project</option>
          </select>
        </div>

        <div class="form-group">
          <label for="project-url">{{ projectUrlLabel }}:</label>
          <input 
            id="project-url"
            v-model="formData.projectUrl"
            type="url" 
            :placeholder="projectUrlPlaceholder"
            required
            :disabled="isSubmitting"
          />
          <small>{{ projectUrlHint }}</small>
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
              {{ isUpdate ? 'Update Submission' : 'Submit Project' }}
            </span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'UploadForm',
  props: {
    classId: {
      type: Number,
      required: true
    },
    weekNumber: {
      type: Number,
      required: true
    },
    existingSubmission: {
      type: Object,
      default: null
    },
    studentId: {
      type: Number,
      default: 1 // Default student ID for demo purposes
    }
  },
  data() {
    return {
      formData: {
        projectType: 'scratch',
        projectUrl: '',
        comment: ''
      },
      isSubmitting: false,
      error: null
    }
  },
  computed: {
    isUpdate() {
      return this.existingSubmission !== null
    },
    isValidUrl() {
      const url = this.formData.projectUrl.trim();
      if (!url) return false;

      if (this.formData.projectType === 'scratch') {
        return url.startsWith('https://scratch.mit.edu/projects/');
      } else if (this.formData.projectType === 'canva') {
        return url.startsWith('https://www.canva.com/design/');
      }
      return false;
    },
    projectUrlLabel() {
      return this.formData.projectType === 'scratch' ? 'Scratch Project URL' : 'Canva Project URL';
    },
    projectUrlPlaceholder() {
      return this.formData.projectType === 'scratch' 
        ? 'https://scratch.mit.edu/projects/123456' 
        : 'https://www.canva.com/design/your-design-id/view';
    },
    projectUrlHint() {
      return this.formData.projectType === 'scratch'
        ? 'Please enter the full URL to your Scratch project'
        : 'Please enter the shareable URL of your Canva project';
    }
  },
  created() {
    // Pre-fill form if updating an existing submission
    if (this.existingSubmission) {
      this.formData.projectUrl = this.existingSubmission.project_url
      this.formData.comment = this.existingSubmission.comment || ''
    }
  },
  methods: {
    async submitForm() {
      if (!this.isValidUrl) {
        this.error = `Please enter a valid ${this.formData.projectType === 'scratch' ? 'Scratch' : 'Canva'} project URL`;
        return;
      }
      
      try {
        this.isSubmitting = true
        this.error = null
        
        const response = await fetch(
          `http://localhost:5000/api/classes/${this.classId}/weeks/${this.weekNumber}/submissions`, 
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              student_id: this.studentId,
              project_type: this.formData.projectType,
              project_url: this.formData.projectUrl,
              comment: this.formData.comment || null
            })
          }
        )
        
        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.error || 'Failed to submit project')
        }
        
        const submission = await response.json()
        this.$emit('submission-complete', submission)
      } catch (err) {
        this.error = err.message
        console.error('Submission error:', err)
      } finally {
        this.isSubmitting = false
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
