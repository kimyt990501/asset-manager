<template>
  <div id="app">
    <nav class="navbar glass-panel">
      <div class="nav-brand">
        <h2>💰 Asset Manager</h2>
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
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  position: sticky;
  top: 0;
  z-index: var(--z-sticky);
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

.nav-right {
  display: flex;
  align-items: center;
  gap: 1.5rem;
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


