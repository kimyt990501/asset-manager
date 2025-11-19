<template>
  <div class="account-list">
    <AccountCard
      v-for="(account, index) in accounts"
      :key="account.id"
      :account="account"
      :style="{ animationDelay: `${index * 0.05}s` }"
      class="account-card-animate"
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

.account-card-animate {
  animation: listItemFadeIn 0.5s ease-out both;
}

@keyframes listItemFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@media (max-width: 768px) {
  .account-list {
    grid-template-columns: 1fr;
  }
}
</style>
