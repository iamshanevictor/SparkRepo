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
        <tr v-for="sub in submissions" :key="sub.id">
          <td>{{ sub.student_name }}</td>
          <td>Week {{ sub.week_number }}: {{ sub.week_title }}</td>
          <td>
            <a :href="sub.project_url" target="_blank" rel="noopener noreferrer">
              {{ sub.project_url.substring(0, 30) }}...
            </a>
          </td>
          <td>
            <span :class="['status', sub.status]">
              {{ sub.status.charAt(0).toUpperCase() + sub.status.slice(1) }}
            </span>
          </td>
          <td>{{ formatDate(sub.submitted_at) }}</td>
          <td>
            <button class="edit-btn" @click="$emit('review', sub)">Review</button>
            <button class="delete-btn" @click="$emit('delete', sub)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'SubmissionsTable',
  props: {
    submissions: { type: Array, required: true },
  },
  methods: {
    formatDate(isoString) {
      if (!isoString) return 'N/A'
      const date = new Date(isoString)
      return date.toLocaleString()
    },
  },
}
</script>

<style scoped>
.status { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 14px; }
.status.submitted { background-color: #e3f2fd; color: #1565c0; }
.status.approved { background-color: #e8f5e9; color: #2e7d32; }
.status.rejected { background-color: #ffebee; color: #c62828; }
.edit-btn, .delete-btn { padding: 4px 8px; border: none; border-radius: 4px; cursor: pointer; margin-right: 5px; }
.edit-btn { background-color: #2196F3; color: white; }
.delete-btn { background-color: #f44336; color: white; }
</style>
