<template>
  <div class="account-list">
    <AccountCard
      v-for="account in accounts"
      :key="account.id"
      :account="account"
      @edit="handleEdit(account)"
      @delete="handleDelete(account)"
    />
  </div>
</template>

<script setup lang="ts">
import type { Account } from '@/types'
import AccountCard from './AccountCard.vue'

interface Props {
  accounts: Account[]
}

defineProps<Props>()

const emit = defineEmits<{
  edit: [account: Account]
  delete: [account: Account]
}>()

const handleEdit = (account: Account) => {
  emit('edit', account)
}

const handleDelete = (account: Account) => {
  emit('delete', account)
}
</script>

<style scoped>
.account-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .account-list {
    grid-template-columns: 1fr;
  }
}
</style>
