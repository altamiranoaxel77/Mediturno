<template>
  <div class="welcome-container">
    <div class="welcome-card">
      <div class="icon-circle">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-12 h-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
      <h1 class="welcome-title">¡Bienvenido, estás dentro del sistema!</h1>
      <p class="welcome-subtitle">
        Has ingresado correctamente al panel de <strong>Mediturno</strong>. 
        Desde aquí podrás gestionar todos los recursos del sistema según tu rol.
      </p>
      
      <div class="info-box">
        <p>Utilizá el menú lateral para navegar entre las diferentes secciones disponibles.</p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.welcome-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 60vh; /* Centrado vertical relativo al área de contenido */
}

.welcome-card {
  text-align: center;
  max-width: 600px;
  padding: 3rem;
  background: white;
  border-radius: 20px;
  box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05);
}

.icon-circle {
  width: 80px;
  height: 80px;
  background-color: #eff6ff;
  color: #1d4ed8;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.5rem;
}

.icon-circle svg {
  width: 40px;
  height: 40px;
}

/* CAMBIO DE COLOR DE LETRA PRINCIPAL */
.welcome-title {
  color: #1e293b; /* Azul muy oscuro, casi negro */
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: 1rem;
  letter-spacing: -0.5px;
}

.welcome-subtitle {
  color: #64748b; /* Gris azulado para el subtítulo */
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.info-box {
  background-color: #f8fafc;
  padding: 1rem;
  border-radius: 10px;
  border-left: 4px solid #1d4ed8;
  color: #475569;
  font-size: 0.95rem;
}
</style>