# 🎮 PixelVault Gaming API

Plataforma backend de gestión de usuarios y autenticación segura para videojuegos y comunidades gamer, desarrollada con **Django 6**, **Django REST Framework (DRF)**, **drf-yasg (Swagger/OpenAPI)** y **SimpleJWT**.

Proyecto desarrollado siguiendo el manual *“Desarrollo Full Stack con Django y ReactJS”* (páginas 5 a 12), aplicando personalizaciones temáticas, nuevas funcionalidades y resolviendo **vulnerabilidades críticas de seguridad** presentes en el código base del manual.

---

## 📌 Enlace al Repositorio

* **GitHub Repository:** `https://github.com/juanZantillan13/Practica-4`

---

## 🚀 Características Principales

1. **Tema Personalizado de Videojuegos:**
   - Proyecto nombrado **PixelVault** (sustituyendo el nombre "restaurante" del manual).
   - Documentación Swagger personalizada bajo el título **"PixelVault Gaming API"**.
2. **Modelo de Usuario Gamer Personalizado:**
   - Autenticación por `email` como identificador principal (`USERNAME_FIELD = 'email'`).
   - Campo extra agregado: **`gamertag`** (apodo / identidad del jugador en la plataforma).
   - El campo `gamertag` está integrado en el **Django Admin**, en el **Serializer** y documentado en **Swagger UI**.
3. **Autenticación con JWT (JSON Web Tokens):**
   - Endpoints de login (`/api/v1/auth/token/`) y refresco (`/api/v1/auth/token/refresh/`).
   - Tiempo de vida del token de acceso (`ACCESS_TOKEN_LIFETIME`) configurado explícitamente a **2 horas**.
4. **CRUD de Usuarios y Endpoint de Perfil:**
   - CRUD administrativo completo para `/api/v1/users/` (restringido a `IsAdminUser`).
   - Endpoint de consulta de datos del perfil personal: `/api/v1/auth/me/` (`IsAuthenticated`).

---

## 🛡️ Corrección de Fallas de Seguridad del Manual

El manual original contenía dos vulnerabilidades de seguridad de alta severidad que fueron analizadas y corregidas:

### 1. Fuga de Contraseña Hash en Respuestas de la API
* **Falla en el manual:** En `UserSerializer`, el campo `'password'` estaba incluido en la lista `fields` sin la directiva `write_only: True`. Por lo tanto, al consultar la lista de usuarios (`GET /api/v1/users/`), el detalle de un usuario o el endpoint de perfil (`GET /api/v1/auth/me/`), la API devolvía el hash de la contraseña (`pbkdf2_sha256$...`) en el cuerpo del JSON, exponiendo las credenciales de los usuarios a cualquier consumidor de la API.
* **Solución aplicada:**
  En `users/serializers.py`, se configuró:
  ```python
  extra_kwargs = {
      'password': {
          'write_only': True,
          'required': False
      }
  }
  ```
  De esta forma, la contraseña puede ser enviada para crear o actualizar un usuario, pero **NUNCA** es incluida en las respuestas serializadas de la API.

---

### 2. Sobreescritura Indebida de Contraseña en Actualizaciones Parciales (PATCH/PUT)
* **Falla en el manual:** En `users/views.py`, el método `partial_update` del manual incluía la siguiente lógica:
  ```python
  def partial_update(self, request, *args, **kwargs):
      if "password" in request.data:
          request.data["password"] = make_password(request.data["password"])
      else:
          request.data["password"] = request.user.password  # ⚠️ FALLA GRAVE
      return super().partial_update(request, *args, **kwargs)
  ```
  Si un administrador editaba cualquier dato de un usuario (por ejemplo, su nombre o gamertag) sin enviar una nueva contraseña, el código le asignaba a dicho usuario el hash de la contraseña de **quien realizaba la petición** (`request.user.password`), corrompiendo la cuenta del usuario editado y asignándole la contraseña del administrador.
* **Solución aplicada:**
  Se rediseñó la lógica tanto en `UserSerializer` como en `UserApiViewSet`:
  ```python
  def update(self, instance, validated_data):
      password = validated_data.pop('password', None)
      user = super().update(instance, validated_data)
      if password:
          user.set_password(password)
          user.save()
      return user
  ```
  Si en la petición de actualización **no se incluye contraseña**, el valor se ignora por completo y la contraseña existente del usuario **permanece 100% intacta**.

---

## 🛠️ Instalación y Puesta en Marcha

### Prerrequisitos
- Python 3.10 o superior (probado con Python 3.13)
- Git

### Pasos

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/TU_USUARIO/pixelvault-api.git
   cd pixelvault-api/pixelvault/backend
   ```

2. **Crear y activar el entorno virtual:**
   ```bash
   # En Windows
   python -m venv venv
   .\venv\Scripts\activate

   # En Linux / macOS
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplicar migraciones:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Crear superusuario administrador:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Ejecutar el servidor de desarrollo:**
   ```bash
   python manage.py runserver
   ```
   El servidor estará disponible en `http://127.0.0.1:8000/`.

---

## 🌐 Endpoints de la API

| Método | Endpoint | Descripción | Permisos |
|---|---|---|---|
| `GET` | `/swagger/` | Documentación interactiva Swagger UI | Público |
| `GET` | `/redoc/` | Documentación alternativa ReDoc | Público |
| `POST` | `/api/v1/auth/token/` | Obtención de tokens JWT (`access` y `refresh`) | Público |
| `POST` | `/api/v1/auth/token/refresh/` | Refresco de token JWT | Público |
| `GET` | `/api/v1/auth/me/` | Datos del perfil del usuario autenticado | `IsAuthenticated` (Bearer Token) |
| `GET` | `/api/v1/users/` | Listar todos los usuarios gamers | `IsAdminUser` |
| `POST` | `/api/v1/users/` | Registrar nuevo usuario | `IsAdminUser` |
| `GET` | `/api/v1/users/{id}/` | Detalle de un usuario gamer | `IsAdminUser` |
| `PUT` | `/api/v1/users/{id}/` | Actualización total de usuario | `IsAdminUser` |
| `PATCH` | `/api/v1/users/{id}/` | Actualización parcial (gamertag, nombre, etc.) | `IsAdminUser` |
| `DELETE` | `/api/v1/users/{id}/` | Eliminar usuario | `IsAdminUser` |

---

## 🧪 Ejecución de Pruebas Automatizadas

El proyecto incluye una suite de pruebas que valida el 100% de los requerimientos y correcciones de seguridad:

```bash
cd backend
python verify_tests.py
```

### Resultados de la suite:
- ✅ **Test 1:** Login con JWT correcto y tiempo de vida `ACCESS_TOKEN_LIFETIME` de exactamente 7,200 segundos (2.0 horas).
- ✅ **Test 2:** Consulta a `/api/v1/auth/me/` devuelve campo extra `gamertag` y **NO** expone el hash de contraseña.
- ✅ **Test 3:** Consulta a `/api/v1/users/` valida que ningún usuario expone su hash de contraseña.
- ✅ **Test 4:** Edición de usuario sin contraseña confirma que el hash no se altera, el usuario mantiene su contraseña original y no adquiere la del administrador.
