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
.status { display: inline-block; padding: 4px 8px; border-radius: 4px; font-size: 14px; }
.status.active { background-color: #e8f5e9; color: #2e7d32; }
.status.inactive { background-color: #f5f5f5; color: #757575; }
.edit-btn { padding: 4px 8px; border: none; border-radius: 4px; cursor: pointer; background-color: #2196F3; color: white; }
</style>
