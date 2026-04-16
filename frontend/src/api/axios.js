// Archivo de configuración para Axios: crea una instancia personalizada para interactuar con la API de FastAPI.
// Incluye configuración base y manejo automático de tokens de autenticación.
import axios from 'axios';

const api = axios.create({
  // PRO-TIP: Si usás Windows, a veces '127.0.0.1' es más estable que 'localhost'
  baseURL: 'http://127.0.0.1:8000/api/v1', 
  headers: {
    'Content-Type': 'application/json'
  }
});

// 1. INTERCEPTOR DE PETICIÓN (Lo que ya tenés, está perfecto)
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// 2. INTERCEPTOR DE RESPUESTA (El "Seguro de Vida")
api.interceptors.response.use(
  (response) => response, // Si la respuesta es OK, la deja pasar
  (error) => {
    // Si el backend nos tira un 401 (Token inválido o expirado)
    if (error.response && error.response.status === 401) {
      console.warn("Sesión expirada o inválida. Limpiando...");
      
      // Borramos el token para que el sistema no crea que sigue logueado
      localStorage.removeItem('token');
      localStorage.removeItem('user'); 

      // Opcional: Podés forzar un redireccionamiento al login
      // window.location.href = '/login'; 
    }
    return Promise.reject(error);
  }
);

export default api;