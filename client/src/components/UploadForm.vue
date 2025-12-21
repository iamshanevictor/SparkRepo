<template>
  <div class="upload-form-overlay">
    <div class="upload-form">
      <div class="form-header">
        <h3>Submit Your {{ projectLabel }} Project</h3>
        <button class="close-btn" @click="$emit('close')">×</button>
      </div>

      <div v-if="error" class="error-message">{{ error }}</div>

      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="student-name">Full Name:</label>
          <input
            id="student-name"
            v-model="form.student_name"
            type="text"
            placeholder="Enter your full name"
            required
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="project-url">{{ projectLabel }} Project URL:</label>
          <input
            id="project-url"
            v-model="form.project_url"
            type="url"
            :placeholder="urlPlaceholder"
            required
            :disabled="loading"
          />
          <small>{{ helperText }}</small>
        </div>

        <div class="form-group">
          <label for="comment">Comment (optional):</label>
          <textarea
            id="comment"
            v-model="form.comment"
            placeholder="Add any comments about your project here..."
            rows="3"
            :disabled="loading"
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="$emit('close')" :disabled="loading">Cancel</button>
          <button type="submit" class="submit-btn" :disabled="loading || !validUrl">
            <span v-if="loading"><span class="spinner"></span> Submitting...</span>
            <span v-else>Submit Project</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { api } from '../api'

export default {
  name: 'UploadForm',
  props: {
    categoryId: { type: String, required: true },
    weekNumber: { type: Number, required: true },
    categoryInfo: { type: Object, required: true },
  },
  data() {
    return {
      loading: false,
      error: null,
      form: {
        student_name: '',
        project_url: '',
        comment: '',
      },
    }
  },
  computed: {
    categoryNameLower() {
      return (this.categoryInfo?.name || '').toLowerCase()
    },
    isCanva() {
      return this.categoryNameLower.includes('canva')
    },
    isScratch() {
      return this.categoryNameLower.includes('scratch')
    },
    projectLabel() {
      if (this.isCanva) return 'Canva'
      if (this.isScratch) return 'Scratch'
      return this.categoryInfo?.name || 'Project'
    },
    urlPlaceholder() {
      if (this.isCanva) return 'https://www.canva.com/design/your-design-id/view'
      if (this.isScratch) return 'https://scratch.mit.edu/projects/123456'
      return 'https://example.com/your-project'
    },
    helperText() {
      if (this.isCanva) return 'Please enter the shareable URL of your Canva project'
      if (this.isScratch) return 'Please enter the full URL to your Scratch project'
      return 'Please enter a valid project URL'
    },
    validUrl() {
      const url = (this.form.project_url || '').trim()
      if (!url) return false
      if (this.isCanva) return url.startsWith('https://www.canva.com/design/')
      if (this.isScratch) return url.startsWith('https://scratch.mit.edu/projects/')
      try { new URL(url); return true } catch { return false }
    },
  },
  methods: {
    async submitForm() {
      if (!this.form.student_name.trim()) {
        this.error = 'Please enter your full name.'
        return
      }
      if (!this.validUrl) {
        this.error = 'Please enter a valid project URL.'
        return
      }
      this.loading = true
      this.error = null
      try {
        const payload = {
          student_name: this.form.student_name,
          project_url: this.form.project_url,
          comment: this.form.comment || null,
        }
        const submission = await api.submitProject(this.categoryId, this.weekNumber, payload)
        this.$emit('submission-complete', submission)
      } catch (e) {
        this.error = e.message || 'Failed to submit project'
      } finally {
        this.loading = false
      }
    },
  },
}
</script>

<style scoped>
.upload-form-overlay { position: fixed; inset: 0; background-color: rgba(0,0,0,.5); display: flex; align-items: center; justify-content: center; z-index: 1000; }
.upload-form { background: #fff; border-radius: 8px; width: 90%; max-width: 520px; padding: 24px; box-shadow: 0 4px 20px rgba(0,0,0,.15); }
.form-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.close-btn { background: none; border: none; font-size: 22px; cursor: pointer; color: #6c757d; }
.form-group { margin-bottom: 16px; }
label { display: block; margin-bottom: 6px; font-weight: 500; }
input, textarea { width: 100%; padding: 10px; border: 1px solid #ced4da; border-radius: 4px; font-size: 16px; }
small { display: block; margin-top: 4px; color: #6c757d; font-size: 12px; }
.form-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 20px; }
.cancel-btn { background: #f8f9fa; border: 1px solid #ced4da; color: #212529; padding: 10px 16px; border-radius: 4px; }
.submit-btn { background: #4CAF50; color: #fff; border: none; padding: 10px 16px; border-radius: 4px; }
.submit-btn:disabled { background: #8bc34a; opacity: .8; cursor: not-allowed; }
.spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: #fff; animation: spin 1s linear infinite; margin-right: 6px; }
@keyframes spin { to { transform: rotate(360deg) } }
</style>
