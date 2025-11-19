<template>
  <form @submit.prevent="handleSubmit">
    <!-- Type Selection -->
    <div class="form-group">
      <label class="label">Type</label>
      <div class="type-selector">
        <button 
          type="button"
          class="type-btn"
          :class="{ active: form.type === 'expense' }"
          @click="form.type = 'expense'"
        >
          Expense
        </button>
        <button 
          type="button"
          class="type-btn"
          :class="{ active: form.type === 'income' }"
          @click="form.type = 'income'"
        >
          Income
        </button>
      </div>
    </div>

    <BaseInput 
      v-model="form.amount" 
      label="Amount" 
      type="number" 
      placeholder="0" 
      required
    />

    <!-- Category Dropdown (Mock for now) -->
    <div class="form-group">
      <label class="label">Category</label>
      <select v-model="form.category_id" class="base-select">
        <option value="" disabled>Select Category</option>
        <option value="1">Food (Variable)</option>
        <option value="2">Rent (Fixed)</option>
        <option value="3">Salary (Income)</option>
      </select>
    </div>

    <BaseInput 
      v-model="form.transaction_date" 
      label="Date" 
      type="date" 
      required
    />

    <BaseInput 
      v-model="form.description" 
      label="Description" 
      placeholder="What was this for?" 
    />

    <div class="form-actions">
      <BaseButton type="button" variant="ghost" @click="$emit('cancel')">Cancel</BaseButton>
      <BaseButton type="submit" variant="primary">Save Transaction</BaseButton>
    </div>
  </form>
</template>

<script setup lang="ts">
import { reactive } from 'vue'
import BaseInput from '../ui/BaseInput.vue'
import BaseButton from '../ui/BaseButton.vue'

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  type: 'expense',
  amount: '',
  category_id: '',
  transaction_date: new Date().toISOString().split('T')[0],
  description: ''
})

const handleSubmit = () => {
  // In a real app, we would validate and call API here
  console.log('Submitting transaction:', form)
  emit('submit', { ...form })
}
</script>

<style scoped>
.form-group {
  margin-bottom: var(--spacing-md);
}

.label {
  display: block;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--text-main);
  margin-bottom: var(--spacing-xs);
}

.type-selector {
  display: flex;
  background: var(--background);
  padding: 4px;
  border-radius: var(--radius-md);
}

.type-btn {
  flex: 1;
  padding: var(--spacing-sm);
  border: none;
  background: transparent;
  border-radius: var(--radius-sm);
  cursor: pointer;
  font-weight: 500;
  color: var(--text-muted);
  transition: var(--transition-base);
}

.type-btn.active {
  background: var(--surface);
  color: var(--primary);
  box-shadow: var(--shadow-sm);
}

.base-select {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--border);
  border-radius: var(--radius-md);
  font-size: 1rem;
  background: var(--surface);
  color: var(--text-main);
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: var(--spacing-md);
  margin-top: var(--spacing-lg);
}
</style>
