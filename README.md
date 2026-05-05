# fastapi-tienda-backend

Backend de una tienda desarrollado con **FastAPI** y **Python**. Es un proyecto sencillo que me sirvió para aprender los fundamentos de:

- Autenticación y autorización con **JWT**
- Validación de payloads con **Pydantic**
- Conexión a base de datos con **SQLAlchemy**
- Subida de archivos a la nube con **Cloudinary**
- Envío de correos via **SMTP**

No es un proyecto de producción ni pretende serlo — fue una base de aprendizaje para entender cómo funciona un backend REST con Python.

---

## Requisitos

- Python 3.9+
- MySQL 8.0+
- Cuenta en [Cloudinary](https://cloudinary.com) (gratuita)
- Cuenta SMTP para envío de correos (ej. [Mailtrap](https://mailtrap.io))

---

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/rcedenod/fastapi-tienda-backend.git
cd fastapi-tienda-backend

# Crear entorno virtual
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

---

## Configuración

### 1. Variables de entorno

Copia el archivo de ejemplo y completa los valores:

```bash
cp .env.example .env
```

| Variable | Descripción |
|---|---|
| `DATABASE_URI` | URI de conexión a MySQL |
| `BCRYPT_SALT` | Cualquier valor (variable reservada, no se usa actualmente) |
| `JWT_KEY` | Clave secreta para firmar tokens JWT. Debe ser larga y aleatoria |
| `CLOUDINARY_URL` | URL de credenciales de Cloudinary |

Para generar un `JWT_KEY` seguro:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Base de datos

Restaura el backup incluido en el repositorio (`db/tienda-db-backup.sql`) en MySQL:

- Abre **MySQL Workbench**
- Ve a `Server → Data Import`
- Selecciona **"Import from Self-Contained File"** y elige el archivo `.sql`
- En **Default Target Schema** crea o selecciona tu base de datos
- Haz clic en **Start Import**

#### Datos iniciales requeridos

**Usuario administrador** — necesario para autenticarte y usar la API. Reemplaza los valores y ejecuta en MySQL:

```sql
INSERT INTO `user` (`Fullname`, `Email`, `Password`, `Role`)
VALUES (
  'Tu Nombre',
  'tu_email@ejemplo.com',
  'hash_de_tu_password',  -- ver nota abajo
  1
);
```

Para generar el hash de la contraseña:

```bash
python -c "from bcrypt import hashpw, gensalt; print(hashpw('tu_password'.encode(), gensalt()).decode())"
```

**Configuración de email** — necesario para el endpoint de recuperación de contraseña:

```sql
INSERT INTO `email_config` (`HostAddress`, `HostPort`, `EmailAddress`, `EmailUsername`, `EmailPassword`)
VALUES (
  'smtp.tuservidor.com',  -- ej: live.smtp.mailtrap.io
  587,
  'remitente@tudominio.com',
  'tu_usuario_smtp',      -- ej: "api" para Mailtrap
  'tu_password_o_token'
);
```

> Para desarrollo se recomienda [Mailtrap](https://mailtrap.io) — captura los correos sin enviarlos realmente.
> Para Gmail se requiere activar verificación en dos pasos y generar una **App Password** desde [myaccount.google.com/apppasswords](https://myaccount.google.com/apppasswords).

### 3. Cloudinary

Obtén tus credenciales en [console.cloudinary.com/app/settings/api-keys](https://console.cloudinary.com/app/settings/api-keys) y completa `CLOUDINARY_URL` en tu `.env`:

```
CLOUDINARY_URL=cloudinary://tu_api_key:tu_api_secret@tu_cloud_name
```

---

## Ejecución

```bash
fastapi dev main.py
```

La API estará disponible en `http://localhost:8000`. La documentación interactiva en `http://localhost:8000/docs`.

---

## Estructura del proyecto

```
fastapi-tienda-backend/
├── main.py               # Punto de entrada
├── config/               # Carga de variables de entorno
├── db/                   # Conexión a base de datos y definición de tablas
├── middlewares/          # Middleware de autenticación JWT
├── routes/               # Rutas de la API
│   ├── auth/             # Login y recuperación de contraseña
│   ├── admins/           # Gestión de administradores
│   ├── categories/       # Gestión de categorías
│   ├── products/         # Gestión de productos
│   ├── profile/          # Perfil del usuario autenticado
│   ├── configs/          # Configuración de la empresa (email)
│   └── files/            # Subida y descarga de archivos
├── schemas/              # Modelos Pydantic para validación de payloads
├── utils/                # Utilidades (bcrypt, JWT, logger, generador de contraseñas)
└── downloads/            # Archivos descargados localmente
```

---

## Cómo funciona

### Autenticación — JWT

El flujo de autenticación funciona así:

1. El cliente hace `POST /api/auth/login` con email y contraseña
2. El backend verifica las credenciales contra la base de datos
3. Si son correctas, devuelve un **token JWT** firmado con `JWT_KEY`
4. El cliente incluye ese token en el header `Authorization: Bearer <token>` en cada request posterior

El token contiene el payload completo del usuario (id, email, rol, etc.) codificado y firmado — no se guarda ninguna sesión en el servidor.

### Middleware de autorización

`middlewares/__init__.py` define `JWTBearer`, una clase que extiende `HTTPBearer` de FastAPI. Se aplica como dependencia en todos los routers protegidos:

```python
dependencies=[Depends(JWTBearer())]
```

Cuando llega una request:
1. Extrae el token del header `Authorization`
2. Lo decodifica con `PyJWT` usando `JWT_KEY`
3. Si es válido, almacena el payload en `request.state.session`
4. Si es inválido o no existe, lanza `HTTP 401` o `HTTP 403`

Las rutas acceden al usuario autenticado así:

```python
user = request.state._state['session']
```

### Validación con Pydantic

Cada endpoint que recibe datos define un **schema Pydantic** en `schemas/`. FastAPI valida automáticamente el payload entrante contra ese schema antes de ejecutar la función. Si el payload no cumple, responde con `HTTP 422` sin llegar a ejecutar ninguna lógica.

Ejemplo — para crear un usuario se valida `User`:

```python
class BaseUser(BaseModel):
    fullname: str
    email: EmailStr

class User(BaseUser):
    password: str = Field(min_length=8)
    role: int = Field(ge=1, le=2)
    is_actived: int
    is_deleted: int
    created_at: datetime
```

### Roles

La API maneja dos roles:

| Rol | Valor | Acceso |
|---|---|---|
| Administrador | `1` | Acceso completo a todas las rutas |
| Usuario | `2` | Acceso limitado (perfil propio) |

Las rutas de administración verifican `user['role'] == 1` y retornan `HTTP 401` si no se cumple.

### Subida de archivos — Cloudinary

`POST /api/files/upload/` recibe un archivo multipart, lo sube a Cloudinary con `resource_type="auto"` (acepta imágenes, videos y cualquier tipo de archivo) y guarda la URL segura en la tabla `file` de la base de datos.

---

## Endpoints

Todos los endpoints requieren autenticación JWT excepto los de `/api/auth/`.

### Auth
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/auth/login` | Login — devuelve token JWT |
| `POST` | `/api/auth/password-recovery` | Envía nueva contraseña al email del usuario |

### Admins
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/admins/` | Listar administradores |
| `GET` | `/api/admins/search/{id}` | Obtener administrador por ID |
| `POST` | `/api/admins/create` | Crear administrador |
| `PUT` | `/api/admins/update/{id}` | Actualizar administrador |
| `PUT` | `/api/admins/change-password/{id}` | Cambiar contraseña |
| `DELETE` | `/api/admins/delete/{id}` | Eliminar administrador |

### Categorías
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/categories/` | Listar categorías (paginado) |
| `GET` | `/api/categories/{id}` | Obtener categoría por ID |
| `GET` | `/api/categories/products/{id}` | Productos de una categoría |
| `POST` | `/api/categories/create` | Crear categoría |
| `PUT` | `/api/categories/update/{id}` | Actualizar categoría |
| `DELETE` | `/api/categories/delete/{id}` | Eliminar categoría |

### Productos
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/products/` | Listar productos (paginado + búsqueda) |
| `GET` | `/api/products/search/{id}` | Obtener producto por ID |
| `GET` | `/api/products/comments/{id}` | Comentarios de un producto |
| `POST` | `/api/products/create` | Crear producto |
| `PUT` | `/api/products/update/{id}` | Actualizar producto |
| `DELETE` | `/api/products/delete/{id}` | Eliminar producto |

### Perfil
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/profile/` | Ver perfil del usuario autenticado |
| `PUT` | `/api/profile/update` | Actualizar nombre y email |
| `PUT` | `/api/profile/change-password` | Cambiar contraseña |

### Configuración
| Método | Ruta | Descripción |
|---|---|---|
| `GET` | `/api/configs/` | Ver configuraciones |
| `GET` | `/api/configs/search/{id}` | Ver configuración por ID |
| `PUT` | `/api/configs/update/{id}` | Actualizar configuración |

### Archivos
| Método | Ruta | Descripción |
|---|---|---|
| `POST` | `/api/files/upload/` | Subir archivo a Cloudinary |
| `GET` | `/api/files/download/` | Descargar archivo por URL |

---

## Tecnologías

| Tecnología | Uso |
|---|---|
| [FastAPI](https://fastapi.tiangolo.com) | Framework web |
| [SQLAlchemy](https://www.sqlalchemy.org) | ORM / conexión a BD |
| [Pydantic](https://docs.pydantic.dev) | Validación de datos |
| [PyJWT](https://pyjwt.readthedocs.io) | Tokens JWT |
| [bcrypt](https://pypi.org/project/bcrypt/) | Hash de contraseñas |
| [Cloudinary](https://cloudinary.com) | Almacenamiento de archivos |
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Variables de entorno |
| [uvicorn](https://www.uvicorn.org) | Servidor ASGI |
