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
          <label for="project-url">{{ projectLabel }} Project URL:</label>
          <input
            id="project-url"
            v-model="form.project_url"
            type="url"
            :placeholder="urlPlaceholder"
            required
            :disabled="loading"
            @input="touched.url = true"
            :aria-invalid="Boolean(urlError)"
            aria-describedby="project-url-help project-url-error"
          />
          <small id="project-url-help">{{ helperText }}</small>
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
            v-model="form.comment"
            placeholder="Add any comments about your project here..."
            rows="3"
            :disabled="loading"
          ></textarea>
        </div>

        <div class="form-actions">
          <button type="button" class="cancel-btn" @click="$emit('close')" :disabled="loading">Cancel</button>
          <button type="submit" class="submit-btn" :disabled="loading || !validUrl || !validFullName">
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
  emits: ['close', 'submitted', 'submission-complete'],
  props: {
    categoryId: { type: String, required: true },
    weekNumber: { type: Number, required: true },
    categoryInfo: { type: Object, required: true },
  },
  data() {
    return {
      loading: false,
      error: null,
      attemptedSubmit: false,
      touched: {
        name: false,
        url: false,
      },
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
    normalizedStudentName() {
      return this.normalizeName(this.form.student_name)
    },
    validFullName() {
      // Must include at least two words: "First Last".
      const parts = (this.form.student_name || '')
        .trim()
        .split(/\s+/)
        .filter(Boolean)
      return parts.length >= 2 && parts[0].length > 0 && parts[1].length > 0
    },
    nameError() {
      const name = (this.form.student_name || '').trim()
      if (!name) return 'Name is required.'
      if (!this.validFullName) return 'Needs to be full name (first and last name).'
      return ''
    },
    validUrl() {
      const url = (this.form.project_url || '').trim()
      if (!url) return false
      if (this.isCanva) return url.startsWith('https://www.canva.com/design/')
      if (this.isScratch) return url.startsWith('https://scratch.mit.edu/projects/')
      try { new URL(url); return true } catch { return false }
    },
    urlError() {
      const url = (this.form.project_url || '').trim()
      if (!url) return 'Project link is required.'
      if (this.isCanva && !url.startsWith('https://www.canva.com/design/')) {
        return 'Needs a valid Canva link (starts with https://www.canva.com/design/).'
      }
      if (this.isScratch && !url.startsWith('https://scratch.mit.edu/projects/')) {
        return 'Needs a valid Scratch link (starts with https://scratch.mit.edu/projects/).'
      }
      try {
        // General fallback
        new URL(url)
        return ''
      } catch {
        return 'Needs a valid URL.'
      }
    },
  },
  methods: {
    normalizeName(input) {
      const raw = (input || '').trim()
      if (!raw) return ''

      // Collapse duplicate whitespace first.
      const collapsed = raw.replace(/\s+/g, ' ')

      // Title-case words while preserving hyphens/apostrophes.
      // Examples: "mARy-jANE" -> "Mary-Jane", "o'connor" -> "O'Connor"
      return collapsed
        .split(' ')
        .map((word) => {
          const lower = word.toLowerCase()
          // Split on hyphen/apostrophe but keep delimiters.
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
      this.form.student_name = this.normalizeName(this.form.student_name)
    },
    async submitForm() {
      this.attemptedSubmit = true
      this.normalizeStudentName()

      if (this.nameError) return
      if (!this.validUrl) {
        this.error = 'Please enter a valid project URL.'
        return
      }
      this.loading = true
      this.error = null
      try {
        const payload = {
          student_name: this.normalizedStudentName,
          project_url: this.form.project_url,
          comment: this.form.comment || null,
        }
        const submission = await api.submitProject(this.categoryId, this.weekNumber, payload)
        // Keep both events for backwards compatibility.
        this.$emit('submission-complete', submission)
        this.$emit('submitted', submission)
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
.field-error { margin-top: 6px; color: #dc2626; font-weight: 700; font-size: 0.85rem; }
.form-actions { display: flex; justify-content: flex-end; gap: 12px; margin-top: 20px; }
.cancel-btn { background: #f8f9fa; border: 1px solid #ced4da; color: #212529; padding: 10px 16px; border-radius: 4px; }
.submit-btn { background: #4CAF50; color: #fff; border: none; padding: 10px 16px; border-radius: 4px; }
.submit-btn:disabled { background: #8bc34a; opacity: .8; cursor: not-allowed; }
.spinner { display: inline-block; width: 16px; height: 16px; border: 2px solid rgba(255,255,255,.3); border-radius: 50%; border-top-color: #fff; animation: spin 1s linear infinite; margin-right: 6px; }
@keyframes spin { to { transform: rotate(360deg) } }
</style>
