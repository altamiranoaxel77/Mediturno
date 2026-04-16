<template>
  <div class="login-page-container">
    <div class="background-decorations">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>

    <div class="login-content-wrapper">
      <div class="login-card">
        <div class="login-header">
          <div class="brand-logo-container">
            <svg class="brand-svg-icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M7 12H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              <path d="M12 7V17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          <h1 class="brand-title">Mediturno</h1>
          <p class="brand-subtitle">Portal Centralizado de Centros de Salud</p>
        </div>

        <transition name="fade">
          <div v-if="errorMessage" class="alert-error" role="alert">
            <svg class="icon-alert" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
            </svg>
            <span>{{ errorMessage }}</span>
          </div>
        </transition>

        <form @submit.prevent="onSubmit" class="login-form">
          <div class="form-group">
            <label for="email">Identificación de Usuario (Email)</label>
            <div class="input-with-icon">
              <svg class="input-icon" viewBox="0 0 20 20" fill="currentColor">
                <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
              </svg>
              <input 
                type="email" 
                id="email" 
                v-model="email" 
                placeholder="ejemplo@gmail.com" 
                required 
                :disabled="authStore.loading"
                autocomplete="username"
              />
            </div>
          </div>

          <div class="form-group">
            <div class="label-row">
              <label for="password">Contraseña de Acceso</label>
            </div>
            <div class="input-with-icon">
              <svg class="input-icon" viewBox="0 0 20 20" fill="currentColor">
                <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 012 2v5a2 2 0 012 2H5a2 2 0 012-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
              </svg>
              <input 
                type="password" 
                id="password" 
                v-model="password" 
                placeholder="••••••••••" 
                required 
                :disabled="authStore.loading"
                autocomplete="current-password"
              />
            </div>
          </div>

          <button type="submit" class="btn-primary" :class="{'btn-loading': authStore.loading}" :disabled="authStore.loading">
            <div v-if="authStore.loading" class="spinner"></div>
            <span v-else>Iniciar Sesión</span>
          </button>
        </form>

        <div class="login-footer">
          <p>Al ingresar, usted acepta los términos de uso y políticas de seguridad.</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const router = useRouter();
const authStore = useAuthStore();

const email = ref('');
const password = ref('');
const errorMessage = ref('');

const onSubmit = async () => {
  errorMessage.value = '';
  try {
    await authStore.login(email.value, password.value);
    
    const rol = authStore.user?.rol?.nombre;

    if (rol === 'SuperAdmin') {
      router.push({ name: 'dashboard-superadmin' });
    } else if (rol === 'Admin') {
      router.push({ name: 'dashboard-admin' });
    } else if (rol === 'Secretario') {
      router.push({ name: 'dashboard-secretario' });
    } else if (rol === 'Doctor') {
      router.push({ name: 'agenda-medica' });
    } else {
      errorMessage.value = 'Rol de usuario no reconocido por el sistema.';
    }

  } catch (error) {
    console.error("Login Error:", error);
    if (error.response) {
      if (error.response.status === 401 || error.response.status === 404) {
        errorMessage.value = 'Credenciales no válidas. Revise su email y contraseña.';
      } else {
        errorMessage.value = `Error del servidor (${error.response.status}). Intente más tarde.`;
      }
    } else if (error.request) {
      errorMessage.value = 'No se pudo conectar con el servidor. ¿Está el backend encendido?';
    } else {
      errorMessage.value = 'Error inesperado. Intente nuevamente.';
    }
  }
};
</script>

<style scoped>
/* Reset Local y Variables */
.login-page-container {
  --color-primary: #1d4ed8;
  --color-primary-hover: #1e40af;
  --color-text-main: #1e293b;
  --color-text-muted: #64748b;
  --color-border: #cbd5e1;
  
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f9ff 0%, #dbeafe 100%);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', sans-serif;
  margin: 0;
  padding: 1.5rem;
}

/* Decoraciones */
.background-decorations {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0;
}
.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(29, 78, 216, 0.05);
}
.circle-1 { width: 400px; height: 400px; top: -100px; left: -100px; }
.circle-2 { width: 600px; height: 600px; bottom: -150px; right: -150px; }

/* Card Principal */
.login-content-wrapper {
  display: flex;
  justify-content: center;
  width: 100%;
  position: relative;
  z-index: 10;
}

.login-card {
  background: white;
  width: 100%;
  max-width: 500px;
  border-radius: 16px;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
  padding: 3rem;
  border: 1px solid rgba(255, 255, 255, 0.5);
}

/* Header */
.login-header { text-align: center; margin-bottom: 2.5rem; }
.brand-logo-container { color: var(--color-primary); margin-bottom: 1rem; }
.brand-svg-icon { width: 60px; height: 60px; }
.brand-title { font-size: 2.2rem; color: #111827; margin: 0; font-weight: 800; }
.brand-subtitle { color: var(--color-text-muted); margin-top: 0.5rem; }

/* Alertas */
.alert-error {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  background-color: #fef2f2;
  color: #b91c1c;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 1.5rem;
  border: 1px solid #fecaca;
  font-size: 0.9rem;
}
.icon-alert { width: 20px; height: 20px; flex-shrink: 0; }

/* Formulario */
.login-form { display: flex; flex-direction: column; gap: 1.5rem; }
.form-group { display: flex; flex-direction: column; gap: 0.5rem; }
.form-group label { font-size: 0.9rem; font-weight: 600; color: #374151; }

.input-with-icon { position: relative; }
.input-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 20px;
  height: 20px;
  color: #94a3b8;
}

/* CORRECCIÓN DE COLOR DE LETRA */
.form-group input {
  width: 100%;
  padding: 0.85rem 1rem 0.85rem 3rem;
  border: 1.5px solid var(--color-border);
  border-radius: 10px;
  font-size: 1rem;
  color: #1e293b !important; /* Texto oscuro forzado */
  background-color: #ffffff !important;
  outline: none;
  box-sizing: border-box;
  transition: all 0.2s;
}

.form-group input::placeholder {
  color: #94a3b8;
}

.form-group input:focus {
  border-color: var(--color-primary);
  box-shadow: 0 0 0 4px rgba(29, 78, 216, 0.1);
}

/* Botón */
.btn-primary {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-primary);
  color: white;
  padding: 1rem;
  border: none;
  border-radius: 10px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-primary:hover:not(:disabled) { background-color: var(--color-primary-hover); }
.btn-primary:disabled { opacity: 0.6; cursor: not-allowed; }

.spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.login-footer { margin-top: 2rem; padding-top: 1.5rem; border-top: 1px solid #e2e8f0; text-align: center; }
.login-footer p { color: #94a3b8; font-size: 0.8rem; }

/* Responsive */
@media (max-width: 480px) {
  .login-card { padding: 2rem 1.5rem; }
  .brand-title { font-size: 1.8rem; }
}
</style>