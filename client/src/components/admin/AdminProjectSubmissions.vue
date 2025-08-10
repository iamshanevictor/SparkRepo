<template>
  <div>
    <div class="section-header">
      <h3>Project Submissions</h3>
    </div>
    <div v-if="loading" class="loading">Loading submissions...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else-if="items.length === 0" class="no-data">No project submissions found.</div>
    <div v-else class="submissions-list">
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Project Link</th>
            <th>Submitted At</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="sub in items" :key="sub.id">
            <td>{{ sub.name }}</td>
            <td>
              <a :href="sub.project_link" target="_blank" rel="noopener noreferrer">
                {{ sub.project_link }}
              </a>
            </td>
            <td>{{ formatDate(sub.submitted_at) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import { formatDate as formatDateUtil } from '../../utils/date'
export default {
  name: 'AdminProjectSubmissions',
  props: {
    items: { type: Array, required: true },
    loading: { type: Boolean, default: false },
    error: { type: String, default: null },
  },
  methods: {
    formatDate(v) { return formatDateUtil(v) },
  },
}
</script>

<style scoped>
.section-header { margin-bottom: 12px; }
.loading { color: #888; }
.error { color: #c00; }
.no-data { color: #555; font-style: italic; }
</style>
