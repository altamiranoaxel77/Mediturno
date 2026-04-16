// Store de autenticación usando Pinia: maneja el estado del usuario y el token JWT.
// Permite login, logout y persistencia del token en localStorage.

import { defineStore } from 'pinia';
import api from '../api/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('token') || null,
    loading: false
  }),
  
  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email, password) {
      this.loading = true;
      try {
        const response = await api.post('/auth/login', { email, password });
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        
        // Una vez logueados, obtenemos los datos del usuario actual
        await this.fetchCurrentUser();
        return true;
      } catch (error) {
        console.error("Error en el login:", error);
        throw error;
      } finally {
        this.loading = false;
      }
    },

    async fetchCurrentUser() {
      try {
        const response = await api.get('/auth/me');
        this.user = response.data;
      } catch (error) {
        this.logout();
      }
    },

    logout() {
      this.user = null;
      this.token = null;
      localStorage.removeItem('token');
    }
  }
});