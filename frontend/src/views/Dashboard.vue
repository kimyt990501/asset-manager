<template>
  <div class="dashboard">
    <h1 class="page-title">대시보드</h1>

    <Loading v-if="loading && !summary" />

    <div v-else>
      <!-- 요약 정보 -->
      <div class="summary-cards">
        <SummaryCard
          title="총 자산"
          :amount="totalAssets"
          type="assets"
        />
        <SummaryCard
          title="월 고정 수입"
          :amount="monthlyIncome"
          type="income"
        />
        <SummaryCard
          title="월 고정 지출"
          :amount="monthlyExpenses"
          type="expense"
        />
        <SummaryCard
          title="순 현금 흐름"
          :amount="netCashflow"
          type="cashflow"
        />
      </div>

      <!-- 계좌 목록 -->
      <div class="section">
        <div class="section-header">
          <h2>내 계좌</h2>
          <Button variant="primary" @click="goToAccounts">
            전체 보기
          </Button>
        </div>

        <div v-if="accounts.length === 0" class="empty-state">
          <p>등록된 계좌가 없습니다.</p>
          <Button variant="primary" @click="goToAccounts">
            계좌 추가하기
          </Button>
        </div>

        <div v-else class="account-grid">
          <AccountCard
            v-for="account in accounts.slice(0, 4)"
            :key="account.id"
            :account="account"
            @edit="goToAccounts"
          />
        </div>
      </div>

      <!-- 최근 거래 -->
      <div class="section">
        <div class="section-header">
          <h2>최근 거래</h2>
          <Button variant="secondary" @click="goToTransactions">
            전체 보기
          </Button>
        </div>

        <div v-if="recentTransactions.length === 0" class="empty-state">
          <p>최근 거래 내역이 없습니다.</p>
        </div>

        <div v-else class="transactions-list">
          <TransactionItem
            v-for="transaction in recentTransactions"
            :key="transaction.id"
            :transaction="transaction"
            :account-name="getAccountById(transaction.account_id)?.name || '알 수 없음'"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import { useAccountStore } from '@/stores/accountStore'
import { useTransactionStore } from '@/stores/transactionStore'
import SummaryCard from '@/components/summary/SummaryCard.vue'
import AccountCard from '@/components/account/AccountCard.vue'
import TransactionItem from '@/components/transaction/TransactionItem.vue'
import Button from '@/components/common/Button.vue'
import Loading from '@/components/common/Loading.vue'

const router = useRouter()
const accountStore = useAccountStore()
const transactionStore = useTransactionStore()

const {
  summary,
  accounts,
  totalAssets,
  monthlyIncome,
  monthlyExpenses,
  netCashflow,
  getAccountById
} = storeToRefs(accountStore)

const { transactions } = storeToRefs(transactionStore)
const loading = computed(() => accountStore.loading || transactionStore.loading)

const recentTransactions = computed(() => {
  return transactions.value.slice(0, 5)
})

onMounted(async () => {
  await Promise.all([
    accountStore.fetchSummary(),
    transactionStore.fetchTransactions(undefined, 10)
  ])
})

const goToAccounts = () => {
  router.push('/accounts')
}

const goToTransactions = () => {
  router.push('/transactions')
}
</script>

<style scoped>
.dashboard {
  min-height: calc(100vh - 64px - 4rem);
}

.page-title {
  color: #2c3e50;
  margin-bottom: 2rem;
  font-size: 2rem;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.section {
  margin-bottom: 3rem;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-header h2 {
  color: #2c3e50;
  font-size: 1.5rem;
}

.account-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.transactions-list {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.empty-state p {
  color: #7f8c8d;
  margin-bottom: 1.5rem;
  font-size: 1.1rem;
}

@media (max-width: 768px) {
  .summary-cards {
    grid-template-columns: 1fr;
  }

  .account-grid {
    grid-template-columns: 1fr;
  }

  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }
}
</style>
