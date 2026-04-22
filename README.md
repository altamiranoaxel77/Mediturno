# Mediturno 🏥

Sistema de Gestión de Turnos para Centros de Salud.

Aplicación web multi-tenant que permite administrar hospitales, médicos, pacientes, disponibilidades horarias y turnos médicos.

---

## Stack tecnológico

| Capa | Tecnología | Versión |
|------|-----------|---------|
| Backend | Python + FastAPI | Python 3.11 / FastAPI 0.111 |
| Base de datos | PostgreSQL | 18 |
| ORM | SQLAlchemy | 2.0.30 |
| Migraciones | Alembic | 1.13.1 |
| Frontend | Vue.js + Vite | Vue 3 |
| Autenticación | JWT (python-jose + bcrypt) | 3.3.0 / bcrypt 4.0.1 |

---

## Roles del sistema

| Rol | Descripción |
|-----|-------------|
| `SuperAdmin` | Dueño de la aplicación. Crea y gestiona hospitales y sus administradores. No tiene hospital asignado. |
| `Admin` | Administrador de un hospital. Crea médicos, secretarios y gestiona su hospital. |
| `Secretario` | Gestiona turnos, disponibilidades y pacientes de su hospital. |
| `Doctor` | Visualiza su propia agenda de turnos. |

---

## Estructura del proyecto

```
Mediturno/
├── backend/
│   ├── app/
│   │   ├── main.py                  ← Entrada FastAPI, registro de routers
│   │   ├── config.py                ← Variables de entorno (pydantic-settings)
│   │   ├── database.py              ← Engine SQLAlchemy, sesión, Base
│   │   ├── models.py                ← Importación centralizada de todos los modelos
│   │   ├── core/
│   │   │   ├── dependencies.py      ← Autenticación JWT y control de roles
│   │   │   ├── jwt.py               ← Creación y verificación de tokens
│   │   │   ├── security.py          ← Hash y verificación de contraseñas (bcrypt)
│   │   │   ├── roles.py             ← Constantes de roles del sistema
│   │   │   └── seed.py              ← Datos iniciales (roles, días y SuperAdmin)
│   │   └── modules/                 ← Un módulo por entidad del sistema
│   │       ├── auth/
│   │       ├── dia_semana/
│   │       ├── disponibilidad/
│   │       ├── especialidad/
│   │       ├── hospital/
│   │       ├── medico/
│   │       ├── obra_social/
│   │       ├── paciente/
│   │       ├── rol/
│   │       ├── turno/
│   │       └── usuario/
│   ├── migrations/
│   │   ├── versions/                ← Archivos de migración generados por Alembic
│   │   ├── env.py                   ← Lee DATABASE_URL desde el .env
│   │   └── script.py.mako
│   ├── .env                         ← Variables privadas (NO subir al repo)
│   ├── .env.example                 ← Plantilla del .env
│   ├── .gitignore
│   ├── alembic.ini
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── api/
    │   │   └── axios.js             ← Instancia Axios con interceptores JWT
    │   ├── layouts/
    │   │   └── DashboardLayout.vue  ← Layout con sidebar y menú dinámico por rol
    │   ├── router/
    │   │   └── index.js             ← Rutas y guards de autenticación por rol
    │   ├── stores/
    │   │   └── auth.js              ← Store Pinia (login, logout, usuario actual)
    │   └── views/
    │       ├── superadmin/
    │       │   ├── HospitalesView.vue
    │       │   └── AdminsView.vue
    │       ├── admin/
    │       │   ├── MedicosView.vue
    │       │   └── UsuariosView.vue
    │       ├── shared/
    │       │   ├── TurnosView.vue
    │       │   ├── DisponibilidadView.vue
    │       │   └── PacientesView.vue
    │       ├── doctor/
    │       │   └── AgendaView.vue
    │       └── LoginView.vue
    ├── package.json
    └── vite.config.js
```

Cada módulo dentro de `app/modules/` sigue esta estructura interna:

```
modules/turno/
├── __init__.py
├── model.py        ← Modelo SQLAlchemy (define la tabla en la BD)
├── schema.py       ← Schemas Pydantic (valida entrada y salida de datos)
├── repository.py   ← Acceso a base de datos (solo consultas SQL)
├── service.py      ← Lógica de negocio y validaciones
└── router.py       ← Endpoints HTTP (rutas FastAPI)
```

---

## Requisitos previos

- [Python 3.11](https://www.python.org/downloads/)
- [PostgreSQL 18](https://www.postgresql.org/download/)
- [Node.js 18+](https://nodejs.org/)
- [Git](https://git-scm.com/)
- [pgAdmin 4](https://www.pgadmin.org/) — opcional pero recomendado

---

## Instalación — Backend

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

#### Opción A — desde psql

**Windows**
```bash
psql -U postgres
CREATE DATABASE mediturno;
\q
```

> **Nota Windows:** Si `psql` no se reconoce, agregá `C:\Program Files\PostgreSQL\18\bin` al PATH del sistema y reiniciá la terminal.

**macOS / Linux**
```bash
sudo -u postgres psql
CREATE DATABASE mediturno;
\q
```

#### Opción B — desde pgAdmin 4

1. Abrir pgAdmin 4 e iniciar sesión.
2. Panel izquierdo: **Servers → PostgreSQL → Databases**.
3. Clic derecho sobre **Databases** → **Create** → **Database...**
4. Campo **Database**: `mediturno` — **Owner**: `postgres` → **Save**.

---

### 3. Crear el entorno virtual

**Windows**
```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

**macOS / Linux**
```bash
python3.11 -m venv venv
source venv/bin/activate
```

> El prompt debe mostrar `(venv)` al inicio.
> En VS Code: `Ctrl+Shift+P` → **Python: Select Interpreter** → elegir el intérprete de la carpeta `venv`.

---

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

> **Importante:** el proyecto requiere `bcrypt==4.0.1` para compatibilidad con passlib. Si tenés una versión distinta:
> ```bash
> pip uninstall bcrypt -y
> pip install bcrypt==4.0.1
> ```

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

Editá el archivo `.env` con tus datos:

```env
# Formato: postgresql+psycopg2://USUARIO:CONTRASEÑA@HOST:PUERTO/BASE_DE_DATOS
DATABASE_URL=postgresql+psycopg2://postgres:tu_contraseña@localhost:5432/mediturno

# Generá una clave con: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=pega_aqui_la_clave_generada

ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
ENVIRONMENT=development
```

Generar `SECRET_KEY`:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

> ⚠️ **Nunca subas el archivo `.env` al repositorio.**

---

### 6. Aplicar las migraciones

```bash
alembic upgrade head
```

Resultado esperado:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 21260cc607ff, initial tables
INFO  [alembic.runtime.migration] Running upgrade 21260cc607ff -> 002_usuario_hospital_nullable, usuario id_hospital nullable con constraint superadmin
```

Verificar tablas creadas desde psql:
```bash
psql -U postgres -d mediturno -c "\dt"
```

Las 10 tablas del sistema:
```
dia_semana              hospital            medico
disponibilidad_medico   obra_social         paciente
especialidad            rol                 turno
usuario
```

---

### 7. Cargar datos iniciales y crear el SuperAdmin

Este comando hace todo en un solo paso: inserta los 4 roles, los 7 días de la semana y crea el usuario SuperAdmin. **Se ejecuta una sola vez.**

```bash
python -m app.core.seed
```

Resultado esperado:
```
Iniciando seed del sistema Mediturno...
==================================================
[1/3] Roles:
  → Insertando rol: SuperAdmin
  → Insertando rol: Admin
  → Insertando rol: Secretario
  → Insertando rol: Doctor
✓ Roles OK
[2/3] Días de la semana:
  → Insertando día: Lunes
  ...
✓ Días de la semana OK
[3/3] Usuario SuperAdmin:
  → SuperAdmin creado
     Email:    superadmin@mediturno.com
     Password: Admin1234
✓ SuperAdmin OK
==================================================
✓ Seed completado exitosamente
```

> ⚠️ **Cambiá la contraseña del SuperAdmin** después del primer login.
>
> El SuperAdmin no tiene hospital asignado — es el dueño de la plataforma y crea los hospitales desde cero.

---

### 8. Iniciar el servidor

```bash
uvicorn app.main:app --reload --port 8000
```

Resultado esperado:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

| URL | Descripción |
|-----|-------------|
| http://localhost:8000 | Endpoint raíz (health check) |
| http://localhost:8000/docs | Swagger UI — documentación interactiva |
| http://localhost:8000/redoc | ReDoc — documentación alternativa |

---

### 9. Probar el login en Swagger

1. Abrí `http://localhost:8000/docs`
2. Expandí `POST /api/v1/auth/login` → **Try it out**
3. Enviá:
```json
{
  "email": "superadmin@mediturno.com",
  "password": "Admin1234"
}
```
4. Copiá el `access_token` de la respuesta
5. Hacé clic en **Authorize** (arriba a la derecha)
6. Pegá el token en el campo **Value** → **Authorize**
7. Probá `GET /api/v1/auth/me` — debería devolver los datos del SuperAdmin con `id_hospital: null`

---

## Instalación — Frontend

### 1. Instalar dependencias

```bash
cd frontend
npm install
```

### 2. Ejecutar en modo desarrollo

```bash
npm run dev
```

La app estará disponible en `http://localhost:5173`

> El backend debe estar corriendo en `http://127.0.0.1:8000` para que el frontend pueda conectarse. Esto está configurado en `src/api/axios.js`.

---

## Flujo de uso del sistema

```
SuperAdmin
    └── Crea Hospitales       →  POST /api/v1/hospitales
    └── Crea Admins           →  POST /api/v1/usuarios  (id_rol=2, con id_hospital)
            └── Admin crea Médicos      →  POST /api/v1/medicos
            └── Admin crea Secretarios →  POST /api/v1/usuarios  (id_rol=3)
            └── Admin configura disponibilidad → POST /api/v1/disponibilidad
                    └── Secretario registra pacientes   →  POST /api/v1/pacientes
                    └── Secretario registra turnos      →  POST /api/v1/turnos
                    └── Secretario consulta agenda      →  GET  /api/v1/turnos/agenda
                    └── Doctor ve su agenda             →  GET  /api/v1/turnos/agenda
```

---

## Endpoints disponibles

| Método | Endpoint | Rol requerido | Descripción |
|--------|----------|---------------|-------------|
| POST | `/api/v1/auth/login` | Público | Iniciar sesión |
| GET | `/api/v1/auth/me` | Autenticado | Ver usuario actual |
| GET | `/api/v1/hospitales` | SuperAdmin | Listar hospitales |
| POST | `/api/v1/hospitales` | SuperAdmin | Crear hospital |
| PUT | `/api/v1/hospitales/{id}` | SuperAdmin | Actualizar hospital |
| PUT | `/api/v1/hospitales/{id}/desactivar` | SuperAdmin | Baja lógica |
| GET | `/api/v1/usuarios` | SuperAdmin / Admin | Listar usuarios del hospital |
| POST | `/api/v1/usuarios` | SuperAdmin / Admin | Crear usuario |
| PUT | `/api/v1/usuarios/{id}` | SuperAdmin / Admin | Actualizar usuario |
| PUT | `/api/v1/usuarios/{id}/desactivar` | SuperAdmin / Admin | Baja lógica |
| GET | `/api/v1/roles` | Autenticado | Listar roles |
| GET | `/api/v1/especialidades` | Autenticado | Listar especialidades |
| POST | `/api/v1/especialidades` | SuperAdmin | Crear especialidad |
| PUT | `/api/v1/especialidades/{id}` | SuperAdmin | Actualizar especialidad |
| PUT | `/api/v1/especialidades/{id}/desactivar` | SuperAdmin | Baja lógica |
| GET | `/api/v1/obras-sociales` | Autenticado | Listar obras sociales |
| POST | `/api/v1/obras-sociales` | SuperAdmin | Crear obra social |
| PUT | `/api/v1/obras-sociales/{id}` | SuperAdmin | Actualizar obra social |
| PUT | `/api/v1/obras-sociales/{id}/desactivar` | SuperAdmin | Baja lógica |
| GET | `/api/v1/medicos` | Admin / Secretario | Listar médicos del hospital |
| POST | `/api/v1/medicos` | Admin | Registrar médico |
| PUT | `/api/v1/medicos/{id}` | Admin | Actualizar médico |
| PUT | `/api/v1/medicos/{id}/desactivar` | Admin | Baja lógica |
| GET | `/api/v1/pacientes` | Admin / Secretario | Listar pacientes del hospital |
| GET | `/api/v1/pacientes/buscar?dni=` | Admin / Secretario | Buscar paciente por DNI |
| POST | `/api/v1/pacientes` | Admin / Secretario | Registrar paciente |
| PUT | `/api/v1/pacientes/{id}` | Admin / Secretario | Actualizar paciente |
| PUT | `/api/v1/pacientes/{id}/desactivar` | Admin / Secretario | Baja lógica |
| GET | `/api/v1/disponibilidad/medico/{id}` | Admin / Secretario | Ver agenda semanal del médico |
| POST | `/api/v1/disponibilidad` | Admin / Secretario | Configurar disponibilidad |
| PUT | `/api/v1/disponibilidad/{id}` | Admin / Secretario | Modificar disponibilidad |
| PUT | `/api/v1/disponibilidad/{id}/desactivar` | Admin / Secretario | Baja lógica |
| GET | `/api/v1/turnos/disponibles?id_medico=&fecha=` | Admin / Secretario | Consultar slots libres |
| GET | `/api/v1/turnos/agenda?id_medico=&fecha=` | Todos | Ver agenda del día |
| GET | `/api/v1/turnos/paciente/{id}` | Admin / Secretario | Historial del paciente |
| POST | `/api/v1/turnos` | Admin / Secretario | Registrar turno |
| PUT | `/api/v1/turnos/{id}/estado` | Admin / Secretario / Doctor | Cambiar estado del turno |
| PUT | `/api/v1/turnos/{id}` | Admin / Secretario / Doctor | Actualizar datos del turno |

---

## Guía para colaboradores

### Flujo de trabajo con Git

```bash
git checkout main
git pull origin main
git checkout -b feature/nombre-de-la-funcionalidad

git add .
git commit -m "feat: descripcion del cambio"
git push origin feature/nombre-de-la-funcionalidad
# Abrir Pull Request en GitHub
```

### Convención de commits

| Prefijo | Cuándo usarlo |
|---------|--------------|
| `feat:` | Nueva funcionalidad |
| `fix:` | Corrección de un bug |
| `docs:` | Cambios en documentación |
| `refactor:` | Mejora de código sin cambiar funcionalidad |
| `chore:` | Mantenimiento (dependencias, configuración) |

### Migraciones

Si modificás un modelo SQLAlchemy:

```bash
alembic revision --autogenerate -m "descripcion del cambio"
alembic upgrade head

# Revertir última migración:
alembic downgrade -1
```

> ⚠️ Nunca modifiques migraciones ya aplicadas. Siempre creá una nueva.

---

## Variables de entorno — referencia

| Variable | Requerida | Por defecto | Descripción |
|----------|-----------|-------------|-------------|
| `DATABASE_URL` | ✅ Sí | — | URL completa de conexión a PostgreSQL |
| `SECRET_KEY` | ✅ Sí | — | Clave secreta JWT (mín. 32 chars) |
| `ALGORITHM` | No | `HS256` | Algoritmo de firma JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | No | `60` | Expiración del token en minutos |
| `ENVIRONMENT` | No | `development` | `development` o `production` |

---

## Solución de problemas frecuentes

#### `ModuleNotFoundError` al iniciar
```bash
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
pip install -r requirements.txt
```

#### `ValidationError` en `DATABASE_URL`
El `.env` tiene variables con formato incorrecto. Debe contener `DATABASE_URL=postgresql+psycopg2://...` en una sola línea.

#### Error de bcrypt al hashear contraseñas
```bash
pip uninstall bcrypt -y
pip install bcrypt==4.0.1
```

#### `psql` no se reconoce (Windows)
Agregar al PATH: `C:\Program Files\PostgreSQL\18\bin` y reiniciar la terminal.

#### Puerto 5432 en uso
PostgreSQL puede estar corriendo en otro puerto (ej: 5433). Actualizá el puerto en el `.env`:
```
DATABASE_URL=postgresql+psycopg2://postgres:contraseña@localhost:5433/mediturno
```

#### Error 500 al hacer login — `expression 'Rol' failed`
Falta el import de `app.models` en `main.py`. Verificá que exista esta línea:
```python
import app.models  # noqa: F401
```

#### `Multiple head revisions` al correr `alembic upgrade head`
Hay dos migraciones que parten del mismo punto. Verificá con `alembic history`, eliminá el archivo duplicado de `migrations/versions/` y volvé a correr:
```bash
alembic upgrade head
```

---

## Seguridad

| Archivo / Carpeta | Motivo |
|-------------------|--------|
| `.env` | Contraseñas y claves JWT |
| `venv/` | Entorno virtual |
| `__pycache__/` | Archivos compilados |
| `frontend/node_modules/` | Dependencias Node.js |

> 🔒 Si subiste el `.env` por error:
> ```bash
> git rm --cached .env
> git commit -m "chore: remove .env from tracking"
> ```
> Cambiá inmediatamente la `SECRET_KEY` y la contraseña de la BD.