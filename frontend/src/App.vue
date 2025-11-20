<template>
  <div id="app">
    <nav class="navbar glass-panel">
      <div class="nav-container">
        <div class="nav-brand">
          <div class="brand-icon">
            <span>$</span>
          </div>
          <h2>Asset Manager</h2>
        </div>
        <div class="nav-right">
          <div class="nav-links" role="navigation" aria-label="주 메뉴">
            <router-link to="/" class="nav-link" aria-label="대시보드 페이지로 이동">대시보드</router-link>
            <router-link to="/accounts" class="nav-link" aria-label="계좌 페이지로 이동">계좌</router-link>
            <router-link to="/transactions" class="nav-link" aria-label="출입금내역 페이지로 이동">출입금내역</router-link>
            <router-link to="/recurring" class="nav-link" aria-label="고정 지출 목록 페이지로 이동">고정 지출 목록</router-link>
          </div>
          <ThemeToggle />
        </div>
      </div>
    </nav>

    <main class="main-content">
      <router-view v-slot="{ Component, route }">
        <transition name="page" mode="out-in">
          <component :is="Component" :key="route.path" />
        </transition>
      </router-view>
    </main>

    <!-- Toast Container -->
    <ToastContainer />
  </div>
</template>

<script setup lang="ts">
import ToastContainer from './components/ui/ToastContainer.vue'
import ThemeToggle from './components/ui/ThemeToggle.vue'
import { useTheme } from './composables/useTheme'

// 테마 초기화
useTheme()
</script>

<style>
/* Global styles are in style.css */
.navbar {
  position: sticky;
  top: var(--spacing-md);
  z-index: 100;
  background: var(--glass-bg); /* Adaptive Glass Background */
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border: 1px solid var(--border);
  border-radius: var(--radius-full);
  padding: 0.5rem 0; /* Reduced vertical padding */
  box-shadow: var(--shadow-sm);
  max-width: 1200px;
  margin: 0 auto var(--spacing-xl);
}

.nav-container {
  padding: 0 var(--spacing-lg);
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  height: 100%;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem; /* Tight gap */
  text-decoration: none;
}

.brand-icon {
  font-size: 1.25rem;
  background: var(--primary);
  color: white;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md); /* Squircle */
  box-shadow: var(--shadow-sm);
}

.nav-brand h2 {
  margin: 0;
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-main);
  letter-spacing: -0.02em;
}

.nav-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-links {
  display: flex;
  gap: 0.5rem; /* Reduced gap for pill buttons */
}

.nav-links a {
  text-decoration: none;
  color: var(--text-muted);
  font-weight: 600;
  font-size: 0.9rem;
  padding: 0.5rem 1rem; /* Pill padding */
  border-radius: var(--radius-full); /* Pill shape */
  transition: var(--transition-base);
}

.nav-links a:hover {
  color: var(--text-main);
  background: var(--surface-hover);
}

.nav-link.router-link-active {
  color: var(--primary);
  background: var(--primary-light);
  box-shadow: var(--shadow-sm);
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
}
</style>


