<template>
  <div class="accounts-page">
    <div class="page-header">
      <h1>계좌 관리</h1>
      <Button variant="primary" @click="openCreateModal">
        + 계좌 추가
      </Button>
    </div>

    <div v-if="loading && accounts.length === 0" class="accounts-grid">
      <AccountCardSkeleton v-for="i in 4" :key="i" />
    </div>

    <BaseEmptyState
      v-else-if="accounts.length === 0"
      title="등록된 계좌가 없습니다"
      description="첫 번째 계좌를 추가하여 자산 관리를 시작하세요."
      action="계좌 추가하기"
      @action="openCreateModal"
    >
      <template #icon>
        <svg xmlns="http://www.w3.org/2000/svg" width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
          <rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect>
          <path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path>
        </svg>
      </template>
    </BaseEmptyState>

    <div v-else>
      <AccountList
        :accounts="accounts"
        @edit="handleEdit"
        @delete="handleDelete"
      />
    </div>

    <!-- Create Modal -->
    <Modal
      :is-open="isCreateModalOpen"
      title="계좌 추가"
      @close="closeCreateModal"
    >
      <AccountForm
        :loading="formLoading"
        @submit="handleCreate"
        @cancel="closeCreateModal"
      />
    </Modal>

    <!-- Edit Modal -->
    <Modal
      :is-open="isEditModalOpen"
      title="계좌 수정"
      @close="closeEditModal"
    >
      <AccountForm
        :account="selectedAccount || undefined"
        :loading="formLoading"
        @submit="handleUpdate"
        @cancel="closeEditModal"
      />
    </Modal>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { storeToRefs } from 'pinia'
import { useAccountStore } from '@/stores/accountStore'
import { useModal } from '@/composables/useModal'
import { useNotification } from '@/composables/useNotification'
import type { Account, AccountFormData } from '@/types'
import AccountList from '@/components/account/AccountList.vue'
import AccountForm from '@/components/account/AccountForm.vue'
import AccountCardSkeleton from '@/components/account/AccountCardSkeleton.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import Modal from '@/components/ui/BaseModal.vue'
import Button from '@/components/ui/BaseButton.vue'

const accountStore = useAccountStore()
const { accounts, loading } = storeToRefs(accountStore)
const { isOpen: isCreateModalOpen, open: openCreateModal, close: closeCreateModal } = useModal()
const { isOpen: isEditModalOpen, open: openEditModal, close: closeEditModal } = useModal()
const { success, error } = useNotification()

const formLoading = ref(false)
const selectedAccount = ref<Account | null>(null)

onMounted(async () => {
  await accountStore.fetchAccounts()
})

const handleCreate = async (formData: AccountFormData) => {
  formLoading.value = true
  try {
    await accountStore.createAccount(formData)
    success('계좌가 추가되었습니다.')
    closeCreateModal()
  } catch (err) {
    error('계좌 추가에 실패했습니다.')
  } finally {
    formLoading.value = false
  }
}

const handleEdit = (account: Account) => {
  selectedAccount.value = account
  openEditModal()
}

const handleUpdate = async (formData: AccountFormData) => {
  if (!selectedAccount.value) return

  formLoading.value = true
  try {
    await accountStore.updateAccount(selectedAccount.value.id, formData)
    success('계좌가 수정되었습니다.')
    closeEditModal()
    selectedAccount.value = null
  } catch (err) {
    error('계좌 수정에 실패했습니다.')
  } finally {
    formLoading.value = false
  }
}

const handleDelete = async (account: Account) => {
  if (!confirm(`'${account.name}' 계좌를 삭제하시겠습니까?`)) {
    return
  }

  try {
    await accountStore.deleteAccount(account.id)
    success('계좌가 삭제되었습니다.')
  } catch (err) {
    error('계좌 삭제에 실패했습니다.')
  }
}
</script>

<style scoped>
.accounts-page {
  min-height: calc(100vh - 64px - 4rem);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--spacing-lg);
}

.page-header h1 {
  color: var(--text-main);
  font-size: 2rem;
  font-weight: 700;
  letter-spacing: -0.02em;
}

.accounts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-md);
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }

  .accounts-grid {
    grid-template-columns: 1fr;
  }
}
</style>

