// Archivo de configuración del router de Vue.js: define las rutas de la aplicación y protege las rutas que requieren autenticación.
import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../stores/auth';
import LoginView from '../views/LoginView.vue';
import DashboardLayout from '../layouts/DashboardLayout.vue';
const routes = [
  { 
    path: '/login', 
    name: 'login', 
    component: LoginView 
  },
  {
    // Esta ruta engloba a todas las que necesitan el Layout
    path: '/',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      { 
        path: 'superadmin', 
        name: 'dashboard-superadmin', 
        component: () => import('../views/HomeView.vue')
      },
      { 
        path: 'admin', 
        name: 'dashboard-admin', 
        component: () => import('../views/HomeView.vue')
      },
      { 
        path: 'secretaria', 
        name: 'dashboard-secretario', 
        component: () => import('../views/HomeView.vue')
      },
      { 
        path: 'doctor', 
        name: 'agenda-medica', 
        component: () => import('../views/HomeView.vue')
      }
    ]
  },
  // Ruta por defecto si algo falla
  { 
    path: '/:pathMatch(.*)*', // Captura cualquier ruta que no exista
    redirect: '/login' 
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

// Guardia de seguridad estricto
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'login' });
  } else if (to.name === 'login' && authStore.isAuthenticated) {
    // Leemos el rol y lo mandamos a su panel exacto
    const rol = authStore.user?.rol?.nombre;
    
    if (rol === 'SuperAdmin') next({ name: 'dashboard-superadmin' });
    else if (rol === 'Admin') next({ name: 'dashboard-admin' });
    else if (rol === 'Secretario') next({ name: 'dashboard-secretario' });
    else if (rol === 'Doctor') next({ name: 'agenda-medica' });
    else next({ name: 'login' }); // Si hay error, lo dejamos en login
  } else {
    next();
  }
});

export default router;