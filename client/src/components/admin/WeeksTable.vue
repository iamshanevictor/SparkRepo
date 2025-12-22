<template>
  <div class="weeks-list">
    <table>
      <thead>
        <tr>
          <th>Week #</th>
          <th>Class</th>
          <th>Title</th>
          <th>Display Name</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="week in weeks" :key="week.id">
          <td>{{ week.week_number }}</td>
          <td>{{ week.class_name }}</td>
          <td>{{ week.title }}</td>
          <td>{{ week.display_name }}</td>
          <td>
            <span :class="['status', week.is_active ? 'active' : 'inactive']">
              {{ week.is_active ? 'Active' : 'Inactive' }}
            </span>
          </td>
          <td>
            <button class="edit-btn" @click="$emit('edit', week)">Edit</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  name: 'WeeksTable',
  props: {
    weeks: { type: Array, required: true },
  },
}
</script>

<style scoped>
.weeks-list {
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
th:nth-child(1), td:nth-child(1) { width: 6%; }
th:nth-child(2), td:nth-child(2) { width: 12%; }
th:nth-child(3), td:nth-child(3) { width: 34%; }
th:nth-child(4), td:nth-child(4) { width: 30%; }
th:nth-child(5), td:nth-child(5) { width: 10%; }
th:nth-child(6), td:nth-child(6) { width: 8%; text-align: right; }

.status {
  display: inline-flex;
  align-items: center;
  padding: 0.35rem 0.6rem;
  border-radius: 9999px;
  font-size: 0.8rem;
  font-weight: 700;
}

.status.active { background-color: #d1fae5; color: #065f46; }
.status.inactive { background-color: #f3f4f6; color: #6b7280; }

.edit-btn {
  padding: 0.45rem 0.75rem;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  background: #2563eb;
  color: white;
  font-weight: 700;
  font-size: 0.85rem;
}

.edit-btn:hover {
  background: #1d4ed8;
}
</style>
