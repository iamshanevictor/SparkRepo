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
          <td>
            <span v-if="sub.week_number || sub.week_title">
              Week {{ sub.week_number || '—' }}<span v-if="sub.week_title">: {{ sub.week_title }}</span>
            </span>
            <span v-else>—</span>
          </td>
          <td>
            <a :href="sub.project_url" target="_blank" rel="noopener noreferrer">
              {{ sub.project_url }}
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
.submissions-list {
  width: 100%;
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  table-layout: fixed;
}

th, td {
  padding: 0.75rem 1rem;
  text-align: left;
  vertical-align: middle;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

th {
  font-weight: 700;
  color: #374151;
  text-transform: uppercase;
  font-size: 0.75rem;
  letter-spacing: 0.06em;
  border-bottom: 1px solid #e5e7eb;
}

td {
  color: #111827;
  font-size: 0.9rem;
  border-bottom: 1px solid #f3f4f6;
}

tbody tr:hover td {
  background: #f9fafb;
}

/* Spread columns across full width */
th:nth-child(1), td:nth-child(1) { width: 18%; }
th:nth-child(2), td:nth-child(2) { width: 24%; }
th:nth-child(3), td:nth-child(3) { width: 26%; }
th:nth-child(4), td:nth-child(4) { width: 10%; }
th:nth-child(5), td:nth-child(5) { width: 14%; }
th:nth-child(6), td:nth-child(6) { width: 8%; text-align: right; }

a {
  display: inline-block;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  color: #2563eb;
  text-decoration: none;
  font-weight: 600;
}

a:hover {
  text-decoration: underline;
}

.status {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 700;
  text-transform: capitalize;
}

.status.submitted { background-color: #dbeafe; color: #1e40af; }
.status.approved { background-color: #d1fae5; color: #065f46; }
.status.rejected { background-color: #fee2e2; color: #991b1b; }

.edit-btn, .delete-btn {
  padding: 0.45rem 0.65rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  margin-left: 0.35rem;
  font-weight: 700;
  font-size: 0.8rem;
}

.edit-btn { background-color: #2563eb; color: white; }
.edit-btn:hover { background-color: #1d4ed8; }

.delete-btn { background-color: #dc2626; color: white; }
.delete-btn:hover { background-color: #b91c1c; }
</style>
