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
| `SuperAdmin` | Dueño de la aplicación. Crea y gestiona hospitales y sus administradores |
| `Admin` | Administrador de un hospital. Crea médicos y secretarios dentro de su hospital |
| `Secretario` | Gestiona turnos, disponibilidades y pacientes de su hospital |
| `Doctor` | Visualiza su propia agenda de turnos |

---

## Estructura del proyecto

```
Mediturno/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  ← Entrada FastAPI, registro de routers
│   │   ├── config.py                ← Variables de entorno (pydantic-settings)
│   │   ├── database.py              ← Engine SQLAlchemy, sesión, Base
│   │   ├── models.py                ← Importación centralizada de todos los modelos
│   │   ├── core/
│   │   │   ├── dependencies.py      ← Autenticación JWT y control de roles
│   │   │   ├── jwt.py               ← Creación y verificación de tokens
│   │   │   ├── security.py          ← Hash y verificación de contraseñas (bcrypt)
│   │   │   ├── roles.py             ← Constantes de roles del sistema
│   │   │   ├── seed.py              ← Datos iniciales (roles y días de semana)
│   │   │   └── crear_superadmin.py  ← Script para crear el primer SuperAdmin
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
└── frontend/                        ← Aplicación Vue.js (próximamente)
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
psql -U postgres
CREATE DATABASE mediturno;
\l
\q
```

> **Nota Windows:** Si `psql` no se reconoce, agregá `C:\Program Files\PostgreSQL\18\bin` al PATH del sistema y reiniciá la terminal.

**macOS / Linux**
```bash
sudo -u postgres psql
CREATE DATABASE mediturno;
\l
\q
```

#### Opción B — desde pgAdmin 4

1. Abrir pgAdmin 4 e iniciar sesión.
2. Panel izquierdo: **Servers → PostgreSQL → Databases**.
3. Clic derecho sobre **Databases** → **Create** → **Database...**
4. Campo **Database**: `mediturno`
5. **Owner**: tu usuario (generalmente `postgres`).
6. Clic en **Save**.

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

### 6. Crear la estructura de módulos

> Si clonás el repositorio, las carpetas ya existen. Solo necesario al inicializar desde cero.

**Windows (PowerShell)**
```powershell
New-Item -ItemType Directory -Force -Path app\core, app\modules\rol, app\modules\hospital, app\modules\especialidad, app\modules\obra_social, app\modules\dia_semana, app\modules\usuario, app\modules\medico, app\modules\paciente, app\modules\disponibilidad, app\modules\turno, app\modules\auth

$modules = @("", "\rol", "\hospital", "\especialidad", "\obra_social", "\dia_semana", "\usuario", "\medico", "\paciente", "\disponibilidad", "\turno", "\auth"); foreach ($m in $modules) { New-Item -Force -Path "app\modules$m\__init__.py" -ItemType File | Out-Null }
New-Item -Force -Path app\core\__init__.py -ItemType File | Out-Null
```

**macOS / Linux**
```bash
mkdir -p app/core app/modules/{rol,hospital,especialidad,obra_social,dia_semana,usuario,medico,paciente,disponibilidad,turno,auth}
touch app/core/__init__.py app/modules/__init__.py
touch app/modules/{rol,hospital,especialidad,obra_social,dia_semana,usuario,medico,paciente,disponibilidad,turno,auth}/__init__.py
```

---

### 7. Aplicar las migraciones

```bash
alembic upgrade head
```

Resultado esperado:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 21260cc607ff, initial tables
```

Verificar tablas creadas:

**Desde psql:**
```bash
psql -U postgres -d mediturno -c "\dt"
```

**Desde pgAdmin:** `mediturno → Schemas → public → Tables`

Las 10 tablas del sistema:
```
dia_semana          hospital         medico
disponibilidad_medico   obra_social      paciente
especialidad        rol              turno
usuario
```

---

### 8. Cargar datos iniciales (seed)

Este comando inserta los 4 roles del sistema y los 7 días de la semana. **Se ejecuta una sola vez.**

```bash
python -m app.core.seed
```

Resultado esperado:
```
Iniciando seed...
  → Insertando rol: SuperAdmin
  → Insertando rol: Admin
  → Insertando rol: Secretario
  → Insertando rol: Doctor
✓ Roles OK
  → Insertando día: Lunes
  ...
✓ Días de la semana OK
✓ Seed completado exitosamente
```

---

### 9. Crear el primer usuario SuperAdmin

El SuperAdmin es el dueño de la aplicación. Se crea una sola vez con este script:

```bash
python -m app.core.crear_superadmin
```

Resultado esperado:
```
Usuario SuperAdmin creado correctamente
Email:    superadmin@mediturno.com
Password: Admin1234
```

> ⚠️ **Cambiá la contraseña del SuperAdmin** después del primer login. Las credenciales por defecto son solo para el entorno de desarrollo.

---

### 10. Iniciar el servidor

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

### 11. Probar el login en Swagger

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
7. Probá `GET /api/v1/auth/me` — debería devolver los datos del SuperAdmin

---

## Flujo de uso del sistema

```
SuperAdmin
    └── Crea Hospitales  →  POST /api/v1/hospitales
    └── Crea Admins      →  POST /api/v1/usuarios  (rol=Admin, asignado a un hospital)
            └── Admin crea Médicos     →  POST /api/v1/medicos
            └── Admin crea Secretarios →  POST /api/v1/usuarios  (rol=Secretario)
                    └── Secretario gestiona disponibilidades  →  POST /api/v1/disponibilidad
                    └── Secretario gestiona turnos            →  POST /api/v1/turnos
                    └── Doctor ve su agenda                   →  GET  /api/v1/turnos/mi-agenda
```

---

## Endpoints disponibles

| Método | Endpoint | Rol requerido | Descripción |
|--------|----------|---------------|-------------|
| POST | `/api/v1/auth/login` | Público | Iniciar sesión |
| GET | `/api/v1/auth/me` | Autenticado | Ver usuario actual |
| GET | `/api/v1/hospitales` | SuperAdmin | Listar hospitales |
| GET | `/api/v1/hospitales/{id}` | SuperAdmin | Ver hospital |
| POST | `/api/v1/hospitales` | SuperAdmin | Crear hospital |
| PUT | `/api/v1/hospitales/{id}` | SuperAdmin | Actualizar hospital |
| PUT | `/api/v1/hospitales/{id}/desactivar` | SuperAdmin | Baja lógica |

> Los demás endpoints se irán habilitando a medida que se completen los módulos.

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
El `.env` tiene variables con formato incorrecto. Debe contener `DATABASE_URL=postgresql+psycopg2://...` y no variables separadas como `db_host`, `db_port`, etc.

#### Error de bcrypt al hashear contraseñas
```bash
pip uninstall bcrypt -y
pip install bcrypt==4.0.1
```

#### `psql` no se reconoce (Windows)
Agregar al PATH: `C:\Program Files\PostgreSQL\18\bin` y reiniciar la terminal.

#### Puerto 5432 en uso
PostgreSQL puede correr en otro puerto (ej: 5433). Actualizá el puerto en el `.env`:
```
DATABASE_URL=...@localhost:5433/mediturno
```

#### Error 500 al hacer login — `expression 'Rol' failed`
Falta el import de `app.models` en `main.py`. Verificá que la segunda línea de imports sea:
```python
import app.models  # noqa: F401
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