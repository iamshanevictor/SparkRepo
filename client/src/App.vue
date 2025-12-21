<script>
export default {
  name: 'App',
}
</script>

<template>
  <div class="app">
    <ErrorBoundary>
      <div class="page-shell">
        <router-view />
        <footer class="global-footer">
          Spark © 2025 · Crafted by Shane Victor
        </footer>
      </div>
    </ErrorBoundary>
  </div>
 </template>

<style>
/* Global styles */
:root {
  --primary-color: #4CAF50;
  --secondary-color: #2196F3;
  --background-color: #f5f7fa;
  --text-color: #333;
  --border-color: #e0e0e0;
  --admin-color: #673AB7;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Fredoka', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  line-height: 1.6;
  color: var(--text-color);
  background-color: var(--background-color);
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.page-shell {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.global-footer {
  margin-top: auto;
  padding: 0.75rem 1rem;
  display: flex;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-top: 1px solid rgba(255, 255, 255, 0.2);
  color: #fff;
  font-size: 0.95rem;
}

/* Student view styles */
.student-view {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo-container {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.header-right {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}

.logo {
  height: 3rem;
}

.tagline {
  color: #666;
  margin-bottom: 0.5rem;
}

.admin-btn {
  background-color: var(--admin-color);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: background-color 0.2s;
}

.admin-btn:hover {
  background-color: #5e35b1;
}

main {
  flex: 1;
  padding: 2rem;
}

footer {
  background-color: transparent;
  color: inherit;
  text-align: center;
  padding: 0;
  margin-top: 0;
}

/* Admin view styles */
.admin-view {
  min-height: 100vh;
  background-color: #f8f9fa;
}

/* Week view layout */
.week-container {
  display: flex;
  gap: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.week-sidebar {
  flex: 0 0 200px;
  background-color: white;
  border-radius: 8px;
  padding: 1rem;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: fit-content;
}

.week-content {
  flex: 1;
}

.week-list {
  list-style: none;
  margin-top: 1rem;
}

.week-list li {
  padding: 0.75rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  margin-bottom: 0.5rem;
  transition: background-color 0.2s, color 0.2s;
  text-align: center;
  font-weight: 500;
}

.week-list li:hover {
  background-color: #f0f0f0;
}

.week-list li.active {
  background-color: var(--primary-color);
  color: white;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  header {
    flex-direction: column;
    text-align: center;
    padding: 1rem;
  }
  
  .header-right {
    margin-top: 1rem;
    align-items: center;
  }
  
  .week-container {
    flex-direction: column;
  }
  
  .week-sidebar {
    flex: none;
    width: 100%;
  }
  
  .week-list {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
  }
  
  .week-list li {
    margin-bottom: 0;
  }
}
</style>
