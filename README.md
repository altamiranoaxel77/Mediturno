# Mediturno 🏥

Sistema de Gestión de Turnos para Centros de Salud.

Aplicación web que permite administrar hospitales, médicos, pacientes, disponibilidades horarias y turnos médicos.

---

## Stack tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Backend | Python + FastAPI | Python 3.11 / FastAPI 0.111 |
| Base de datos | PostgreSQL | 18 |
| ORM | SQLAlchemy | 2.0.30 |
| Migraciones | Alembic | 1.13.1 |
| Frontend | Vue.js + Vite | Vue 3 |
| Autenticación | JWT (python-jose + bcrypt) | 3.3.0 |

---

## Requisitos previos

Antes de instalar el proyecto, asegurate de tener lo siguiente instalado:

- [Python 3.11](https://www.python.org/downloads/)
- [PostgreSQL 18](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/)
- [Node.js 18+](https://nodejs.org/) — para el frontend Vue
- [pgAdmin 4](https://www.pgadmin.org/) — opcional pero recomendado

---

## Instalación paso a paso

### 1. Clonar el repositorio

**Windows**
```bash
git clone https://github.com/tu-usuario/mediturno.git
cd mediturno\backend
```

**macOS / Linux**
```bash
git clone https://github.com/tu-usuario/mediturno.git
cd mediturno/backend
```

---

### 2. Crear la base de datos

#### Opción A — desde la consola (psql)

**Windows**
```bash
# Abrir el cliente psql
psql -U postgres

# Dentro del prompt de psql ejecutar:
CREATE DATABASE mediturno;

# Verificar que se creó:
\l

# Salir:
\q
```

> **Nota:** Si `psql` no se reconoce como comando, agregá la carpeta `bin` de PostgreSQL al PATH del sistema. Ejemplo: `C:\Program Files\PostgreSQL\18\bin`

**macOS / Linux**
```bash
# Conectarse como superusuario
sudo -u postgres psql

# Crear la base de datos:
CREATE DATABASE mediturno;

# Verificar:
\l

# Salir:
\q
```

#### Opción B — desde pgAdmin 4

1. Abrir pgAdmin 4 e iniciar sesión con tu contraseña de PostgreSQL.
2. En el panel izquierdo expandir: **Servers → PostgreSQL → Databases**.
3. Clic derecho sobre **Databases** → **Create** → **Database...**
4. En el campo **Database** escribir: `mediturno`
5. En **Owner** seleccionar tu usuario (generalmente `postgres`).
6. Clic en **Save**.

> **Nota:** Verificá que el servicio de PostgreSQL esté corriendo antes de conectarte. En Windows podés comprobarlo en `Servicios (services.msc) → postgresql-x64-18`.

---

### 3. Crear el entorno virtual

**Windows**
```bash
# Crear el entorno virtual con Python 3.11
py -3.11 -m venv venv

# Activar el entorno virtual
venv\Scripts\activate
```

**macOS / Linux**
```bash
# Crear el entorno virtual
python3.11 -m venv venv

# Activar
source venv/bin/activate
```

> Cuando el entorno esté activo, el prompt de la terminal muestra `(venv)` al inicio. En VS Code: `Ctrl+Shift+P` → **Python: Select Interpreter** → elegir el intérprete de la carpeta `venv`.

---

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

---

### 5. Configurar variables de entorno

**Windows**
```bash
copy .env.example .env
```

**macOS / Linux**
```bash
cp .env.example .env
```

Abrí el archivo `.env` y completá con tus datos:

```env
# URL de conexión a PostgreSQL
# Formato: postgresql+psycopg2://USUARIO:CONTRASEÑA@HOST:PUERTO/BASE_DE_DATOS
DATABASE_URL=postgresql+psycopg2://postgres:tu_contraseña@localhost:5432/mediturno

# Clave secreta para firmar los tokens JWT
# Generá una con: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=pega_aqui_la_clave_generada

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=development
```

Para generar una `SECRET_KEY` segura ejecutá:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> ⚠️ **Nunca subas el archivo `.env` al repositorio.** Contiene contraseñas y claves secretas. Ya está incluido en el `.gitignore`.

---

### 6. Ejecutar migraciones

Las migraciones crean todas las tablas en la base de datos automáticamente:

```bash
# Aplicar todas las migraciones pendientes
alembic upgrade head
```

Si es la primera vez que se corre el proyecto y no existe ninguna migración:

```bash
# Generar la migración inicial
alembic revision --autogenerate -m "initial tables"

# Aplicarla
alembic upgrade head
```

---

### 7. Iniciar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

Si ves este mensaje, la instalación fue exitosa:

```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

La API estará disponible en:

| URL | Descripción |
|-----|-------------|
| http://localhost:8000 | Endpoint raíz (health check) |
| http://localhost:8000/docs | Swagger UI — documentación interactiva |
| http://localhost:8000/redoc | ReDoc — documentación alternativa |

---

## Guía para colaboradores

### Flujo de trabajo con Git

```bash
# Nunca trabajar directamente en main
# Siempre crear una rama nueva por cada tarea

# 1. Actualizar main antes de crear la rama
git checkout main
git pull origin main

# 2. Crear y cambiar a la nueva rama
git checkout -b feature/nombre-de-la-funcionalidad

# 3. Hacer commits con mensajes descriptivos
git add .
git commit -m "feat: descripcion del cambio"

# 4. Subir la rama
git push origin feature/nombre-de-la-funcionalidad

# 5. Abrir un Pull Request en GitHub para revisión
```

### Convención de commits

| Prefijo | Cuándo usarlo |
|---------|--------------|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de un bug |
| `docs:` | Cambios en documentación |
| `refactor:` | Mejora de código sin cambiar funcionalidad |
| `chore:` | Mantenimiento (dependencias, configuración) |

### Migraciones — reglas importantes

Si modificás un modelo SQLAlchemy (nueva columna, nueva tabla, etc.) **siempre** generá una nueva migración:

```bash
# 1. Generar la migración
alembic revision --autogenerate -m "descripcion del cambio"

# 2. Revisar el archivo generado en migrations/versions/

# 3. Aplicar la migración
alembic upgrade head

# Para revertir la última migración:
alembic downgrade -1
```

> ⚠️ Nunca modifiques archivos de migración que ya fueron aplicados. Siempre creá uno nuevo.

---

## Variables de entorno — referencia

| Variable | Requerida | Valor por defecto | Descripción |
|----------|-----------|-------------------|-------------|
| `DATABASE_URL` | ✅ Sí | — | URL completa de conexión a PostgreSQL |
| `SECRET_KEY` | ✅ Sí | — | Clave secreta para firmar tokens JWT (mín. 32 chars) |
| `ALGORITHM` | No | `HS256` | Algoritmo de firma JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `60` | Expiración del token en minutos |
| `ENVIRONMENT` | No | `development` | Entorno: `development` o `production` |

---

## Solución de problemas frecuentes

#### `ModuleNotFoundError` al iniciar el servidor
El entorno virtual no está activo o las dependencias no están instaladas.
```bash
# Windows
venv\Scripts\activate
pip install -r requirements.txt

# macOS / Linux
source venv/bin/activate
pip install -r requirements.txt
```

#### `ValidationError` en `DATABASE_URL` al iniciar
El `.env` tiene variables con formato incorrecto. Verificá que contenga `DATABASE_URL=postgresql+psycopg2://...` y no variables separadas como `db_host`, `db_port`, etc.

#### `psql` no se reconoce como comando (Windows)
Agregá la carpeta `bin` de PostgreSQL al PATH del sistema:
`Panel de Control → Sistema → Variables de entorno → Path → Agregar: C:\Program Files\PostgreSQL\18\bin`
Reiniciá la terminal.

#### El puerto 5432 ya está en uso
PostgreSQL puede estar corriendo en un puerto diferente (ej: 5433). Verificalo con:
```bash
# Windows
netstat -an | findstr 5432

# macOS / Linux
sudo lsof -i :5432
```
Luego actualizá el puerto en el `.env`: `DATABASE_URL=...@localhost:5433/mediturno`

#### Los cambios en el código no se reflejan
Verificá que uvicorn esté corriendo con el flag `--reload`:
```bash
uvicorn app.main:app --reload --port 8000
```

---

## Seguridad — archivos que NO deben subirse al repositorio

Los siguientes archivos ya están en el `.gitignore`:

| Archivo / Carpeta | Motivo |
|-------------------|--------|
| `.env` | Contiene contraseñas y claves JWT |
| `venv/` | Entorno virtual — cada dev crea el suyo |
| `__pycache__/` | Archivos compilados de Python |
| `frontend/node_modules/` | Dependencias de Node.js |

> 🔒 Si accidentalmente subiste el `.env` al repositorio:
> ```bash
> git rm --cached .env
> git commit -m "chore: remove .env from tracking"
> ```
> Luego cambiá inmediatamente la `SECRET_KEY` y la contraseña de la base de datos.