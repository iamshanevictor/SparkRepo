<template>
  <div class="weeks-list">
    <table>
      <thead>
        <tr>
          <th>Week #</th>
          <th>Category</th>
          <th>Title</th>
          <th>Display Name</th>
          <th>Status</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="week in weeks" :key="week.id">
          <td>{{ week.week_number }}</td>
          <td>{{ week.category_name || week.class_name }}</td>
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
  name: 'AdminWeeksTable',
  props: {
    weeks: { type: Array, required: true },
  },
}
</script>

<style scoped>
.status.active { color: #2e7d32; }
.status.inactive { color: #9e9e9e; }
.edit-btn { padding: 4px 10px; }
</style>
