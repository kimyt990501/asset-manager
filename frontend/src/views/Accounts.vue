<template>
  <div class="accounts-page">
    <div class="page-header">
      <h1>계좌 관리</h1>
      <Button variant="primary" @click="openCreateModal">
        + 계좌 추가
      </Button>
    </div>

    <Loading v-if="loading && accounts.length === 0" />

    <div v-else-if="accounts.length === 0" class="empty-state">
      <p>등록된 계좌가 없습니다.</p>
      <Button variant="primary" @click="openCreateModal">
        첫 계좌 추가하기
      </Button>
    </div>

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
import Modal from '@/components/ui/BaseModal.vue'
import Button from '@/components/ui/BaseButton.vue'
import Loading from '@/components/common/Loading.vue'

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

.empty-state {
  text-align: center;
  padding: var(--spacing-2xl);
  background: var(--surface);
  border-radius: var(--radius-lg);
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--border-light);
}

.empty-state p {
  color: var(--text-muted);
  margin-bottom: var(--spacing-lg);
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: var(--spacing-md);
  }
}
</style>

