<template>
  <div class="dashboard-container">
    
    <aside class="sidebar">
      <div class="sidebar-header">
        <span class="brand-icon">🏥</span>
        <h2 class="brand-name">Mediturno</h2>
      </div>

      <nav class="sidebar-nav">
        <router-link :to="{ name: 'dashboard-superadmin' }" class="nav-item">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
          Inicio
        </router-link>

        <router-link v-if="userRole === 'SuperAdmin'" to="#" class="nav-item">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"></path></svg>
          Hospitales
        </router-link>
        
        </nav>

      <div class="sidebar-footer">
        <button @click="handleLogout" class="btn-logout">
          <svg class="nav-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"></path><polyline points="16 17 21 12 16 7"></polyline><line x1="21" y1="12" x2="9" y2="12"></line></svg>
          Cerrar Sesión
        </button>
      </div>
    </aside>

    <div class="main-content">
      
      <header class="topbar">
        <div class="page-title">
          <h3>Panel de Control</h3>
        </div>
        
        <div class="user-profile">
          <div class="user-info">
            <span class="user-name">{{ userName }}</span>
            <span class="user-role">{{ userRole }}</span>
          </div>
          <div class="avatar">
            {{ userInitials }}
          </div>
        </div>
      </header>

      <main class="page-content">
        <router-view></router-view>
      </main>

    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

// Datos calculados a partir de Pinia para mostrar en la interfaz
const userName = computed(() => {
  if (!authStore.user) return 'Usuario';
  return `${authStore.user.nombre} ${authStore.user.apellido}`;
});

const userRole = computed(() => {
  return authStore.user?.rol?.nombre || 'Rol no definido';
});

const userInitials = computed(() => {
  if (!authStore.user) return 'U';
  return `${authStore.user.nombre.charAt(0)}${authStore.user.apellido.charAt(0)}`.toUpperCase();
});

// Función para cerrar sesión
const handleLogout = () => {
  authStore.logout();
  router.push({ name: 'login' });
};
</script>

<style scoped>
/* Arquitectura del Dashboard: Flexbox para separar Sidebar del Contenido */
.dashboard-container {
  display: flex;
  height: 100vh;
  background-color: #f8fafc;
  font-family: 'Inter', sans-serif;
  overflow: hidden;
}

/* --- SIDEBAR --- */
.sidebar {
  width: 260px;
  background-color: #ffffff;
  border-right: 1px solid #e2e8f0;
  display: flex;
  flex-direction: column;
  transition: all 0.3s ease;
}

.sidebar-header {
  height: 70px;
  display: flex;
  align-items: center;
  padding: 0 1.5rem;
  border-bottom: 1px solid #e2e8f0;
  gap: 0.75rem;
}

.brand-icon {
  font-size: 1.5rem;
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
}

.sidebar-nav {
  flex: 1;
  padding: 1.5rem 1rem;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  overflow-y: auto;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: #475569;
  text-decoration: none;
  font-weight: 500;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-item:hover, .nav-item.router-link-active {
  background-color: #eff6ff;
  color: #1d4ed8;
}

.nav-icon {
  width: 20px;
  height: 20px;
}

.sidebar-footer {
  padding: 1rem;
  border-top: 1px solid #e2e8f0;
}

.btn-logout {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 0.75rem;
  background-color: transparent;
  color: #ef4444; /* Rojo para acciones destructivas/salida */
  border: 1px solid #fca5a5;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.btn-logout:hover {
  background-color: #fef2f2;
}

/* --- ÁREA PRINCIPAL --- */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* --- TOPBAR --- */
.topbar {
  height: 70px;
  background-color: #ffffff;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 2rem;
}

.page-title h3 {
  margin: 0;
  color: #1e293b;
  font-weight: 600;
}

.user-profile {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.user-info {
  display: flex;
  flex-direction: column;
  text-align: right;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: #1e293b;
}

.user-role {
  font-size: 0.75rem;
  color: #64748b;
  background-color: #f1f5f9;
  padding: 0.1rem 0.5rem;
  border-radius: 12px;
  margin-top: 0.1rem;
  display: inline-block;
}

.avatar {
  width: 40px;
  height: 40px;
  background-color: #1d4ed8;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
}

/* --- CONTENIDO DE LA PÁGINA --- */
.page-content {
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
}
</style>