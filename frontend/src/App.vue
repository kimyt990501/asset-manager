<template>
  <div id="app">
    <nav class="navbar glass-panel">
      <div class="nav-brand">
        <h2>💰 Asset Manager</h2>
      </div>
      <div class="nav-links" role="navigation" aria-label="주 메뉴">
        <router-link to="/" class="nav-link" aria-label="대시보드 페이지로 이동">대시보드</router-link>
        <router-link to="/accounts" class="nav-link" aria-label="계좌 페이지로 이동">계좌</router-link>
        <router-link to="/transactions" class="nav-link" aria-label="출입금내역 페이지로 이동">출입금내역</router-link>
        <router-link to="/recurring" class="nav-link" aria-label="고정 지출 목록 페이지로 이동">고정 지출 목록</router-link>
      </div>
    </nav>

    <main class="main-content">
      <router-view v-slot="{ Component, route }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </main>

    <!-- Quick Add FAB -->
    <button
      class="fab-btn"
      @click="isModalOpen = true"
      aria-label="새 거래 추가"
    >
      <span class="fab-icon">+</span>
    </button>

    <!-- Transaction Modal -->
    <BaseModal
      :isOpen="isModalOpen"
      title="Add Transaction"
      @close="isModalOpen = false"
    >
      <TransactionForm @submit="handleTransactionSubmit" @cancel="isModalOpen = false" />
    </BaseModal>

    <!-- Toast Container -->
    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import BaseModal from './components/ui/BaseModal.vue'
import TransactionForm from './components/domain/TransactionForm.vue'
import ToastContainer from './components/ui/ToastContainer.vue'

const isModalOpen = ref(false)

const handleTransactionSubmit = (data: any) => {
  console.log('Transaction added:', data)
  // TODO: Call API store
  isModalOpen.value = false
}
</script>

<style>
/* Global styles are in style.css */
.navbar {
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  position: sticky;
  top: 0;
  z-index: 100;
  margin-bottom: var(--spacing-md);
}

.nav-brand h2 {
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  font-size: 1.5rem;
  font-weight: 800;
  letter-spacing: -0.02em;
}

.nav-links {
  display: flex;
  gap: 1rem;
}

.nav-link {
  text-decoration: none;
  color: var(--text-muted);
  font-weight: 600;
  padding: 0.6rem 1.2rem;
  border-radius: var(--radius-full);
  transition: var(--transition-base);
  font-size: 0.95rem;
}

.nav-link:hover {
  color: var(--text-main);
  background: rgba(0, 0, 0, 0.03);
}

.nav-link.router-link-active {
  color: var(--primary);
  background: var(--primary-light);
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: var(--spacing-xl);
  width: 100%;
  position: relative;
}

/* Page Transition Animations */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-20px);
}

.page-enter-to,
.page-leave-from {
  opacity: 1;
  transform: translateY(0);
}

/* FAB Styles */
.fab-btn {
  position: fixed;
  bottom: 2.5rem;
  right: 2.5rem;
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-hover) 100%);
  color: white;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  cursor: pointer;
  transition: var(--transition-smooth);
  z-index: 90;
}

.fab-icon {
  font-size: 2.5rem;
  line-height: 1;
  font-weight: 300;
  margin-top: -4px;
}

.fab-btn:hover {
  transform: translateY(-4px) rotate(90deg);
  box-shadow: var(--shadow-xl), var(--shadow-glow);
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    height: auto;
    padding: 1rem;
    gap: 1rem;
  }

  .nav-links {
    gap: 0.5rem;
    flex-wrap: wrap;
    justify-content: center;
  }

  .main-content {
    padding: var(--spacing-md);
  }
  
  .fab-btn {
    bottom: 1.5rem;
    right: 1.5rem;
    width: 56px;
    height: 56px;
  }
}
</style>


