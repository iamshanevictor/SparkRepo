<template>
  <div class="submissions-list">
    <table>
      <thead>
        <tr>
          <th>Student</th>
          <th>Week</th>
          <th>Project URL</th>
          <th>Status</th>
          <th>Submitted</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="sub in items" :key="sub.id">
          <td>{{ sub.student_name }}</td>
          <td>Week {{ sub.week_number }}: {{ sub.week_title }}</td>
          <td>
            <a :href="sub.project_url" target="_blank" rel="noopener noreferrer">
              {{ shorten(sub.project_url) }}
            </a>
          </td>
          <td>
            <span :class="['status', sub.status]">
              {{ capitalize(sub.status) }}
            </span>
          </td>
          <td>{{ formatDate(sub.submitted_at) }}</td>
          <td>
            <button class="edit-btn" @click="$emit('edit', sub)">Review</button>
            <button class="delete-btn" @click="$emit('delete', sub)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { formatDate as formatDateUtil } from '../../utils/date'
export default {
  name: 'AdminSubmissionsTable',
  props: {
    items: { type: Array, required: true },
  },
  methods: {
    formatDate(v) { return formatDateUtil(v) },
    capitalize(s) { return s ? s.charAt(0).toUpperCase() + s.slice(1) : '' },
    shorten(u) { return typeof u === 'string' && u.length > 30 ? `${u.substring(0, 30)}...` : u },
  },
}
</script>

<style scoped>
.status.approved { color: #2e7d32; }
.status.rejected { color: #c62828; }
.status.submitted { color: #1565c0; }
.edit-btn, .delete-btn { padding: 4px 10px; margin-right: 6px; }
</style>
