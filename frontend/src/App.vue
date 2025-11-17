<template>
  <div id="app">
    <nav class="navbar">
      <div class="nav-brand">
        <h2>💰 Asset Manager</h2>
      </div>
      <div class="nav-links">
        <router-link to="/" class="nav-link">대시보드</router-link>
        <router-link to="/accounts" class="nav-link">계좌</router-link>
        <router-link to="/transactions" class="nav-link">거래내역</router-link>
        <router-link to="/recurring" class="nav-link">정기거래</router-link>
      </div>
    </nav>

    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
// App.vue - 메인 레이아웃
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
  background: #f5f6fa;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

.navbar {
  background: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 0 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-brand h2 {
  color: #2c3e50;
  font-size: 1.5rem;
  font-weight: 700;
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  text-decoration: none;
  color: #7f8c8d;
  font-weight: 500;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.nav-link:hover {
  color: #2c3e50;
  background: #f5f6fa;
}

.nav-link.router-link-active {
  color: #3498db;
  background: rgba(52, 152, 219, 0.1);
}

.main-content {
  max-width: 1400px;
  margin: 0 auto;
  padding: 2rem;
}

@media (max-width: 768px) {
  .navbar {
    flex-direction: column;
    height: auto;
    padding: 1rem;
    gap: 1rem;
  }

  .nav-links {
    gap: 1rem;
  }

  .main-content {
    padding: 1rem;
  }
}
</style>
