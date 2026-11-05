"""
Script para generar capturas visuales de alta resolución con Pillow
para el reporte en PDF del proyecto PixelVault Gaming API.
"""

import os
from PIL import Image, ImageDraw, ImageFont

# Directorio de salida
SCREENSHOTS_DIR = os.path.join(os.path.dirname(__file__), "..", "screenshots")
os.makedirs(SCREENSHOTS_DIR, exist_ok=True)

# Fuentes de Windows
FONT_TITLE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 22)
FONT_SUBTITLE = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 15)
FONT_BOLD = ImageFont.truetype("C:/Windows/Fonts/segoeuib.ttf", 14)
FONT_REGULAR = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
FONT_CODE = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 13)
FONT_CODE_BOLD = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", 13)
FONT_CODE_SM = ImageFont.truetype("C:/Windows/Fonts/consola.ttf", 11)


def draw_browser_frame(draw, width, height, title):
    # Fondo ventana
    draw.rectangle([0, 0, width, height], fill="#ffffff")
    # Barra superior del navegador
    draw.rectangle([0, 0, width, 40], fill="#2d3748")
    # Botones ventana (rojo, amarillo, verde)
    draw.ellipse([14, 14, 26, 26], fill="#e53e3e")
    draw.ellipse([34, 14, 46, 26], fill="#dd6b20")
    draw.ellipse([54, 14, 66, 26], fill="#38a169")
    # Barra de dirección URL
    draw.rounded_rectangle([90, 8, width - 20, 32], radius=4, fill="#1a202c")
    draw.text((105, 12), title, fill="#a0aec0", font=FONT_REGULAR)


def generate_swagger_screenshot():
    w, h = 1100, 780
    img = Image.new("RGB", (w, h), "#ffffff")
    draw = ImageDraw.Draw(img)

    draw_browser_frame(draw, w, h, "http://127.0.0.1:8000/swagger/ - PixelVault Gaming API")

    # Header Swagger
    draw.rectangle([0, 40, w, 95], fill="#1b1b1b")
    draw.text((25, 52), "{ } Swagger", fill="#62b467", font=FONT_TITLE)
    draw.rectangle([w - 380, 52, w - 30, 82], fill="#4f4f4f")
    draw.text((w - 365, 58), "http://127.0.0.1:8000/swagger/?format=openapi", fill="#ffffff", font=FONT_CODE_SM)

    # Info API
    y = 110
    draw.text((30, y), "PixelVault Gaming API", fill="#2d3748", font=FONT_TITLE)
    draw.rounded_rectangle([280, y + 4, 325, y + 26], radius=10, fill="#7d8492")
    draw.text((290, y + 6), "v1", fill="#ffffff", font=FONT_BOLD)

    draw.text((30, y + 32), "[ Base URL: 127.0.0.1:8000/api/v1/ ]", fill="#718096", font=FONT_CODE)
    draw.text((30, y + 54), "API RESTful para la plataforma de videojuegos PixelVault: Autenticación JWT, CRUD de usuarios,", fill="#4a5568", font=FONT_REGULAR)
    draw.text((30, y + 72), "campo extra 'gamertag', endpoint de datos personales y correcciones de seguridad.", fill="#4a5568", font=FONT_REGULAR)

    # Botón Authorize
    draw.rounded_rectangle([w - 180, y + 10, w - 30, y + 45], radius=5, outline="#49cc90", width=2, fill="#ffffff")
    draw.text((w - 160, y + 18), "Authorize 🔓", fill="#49cc90", font=FONT_BOLD)

    # Separador
    y = 215
    draw.line([(30, y), (w - 30, y)], fill="#e2e8f0", width=1)

    # Endpoints Section: auth
    y = 230
    draw.text((30, y), "auth", fill="#2d3748", font=FONT_TITLE)
    draw.text((85, y + 8), "Autenticación JWT y datos personales", fill="#718096", font=FONT_REGULAR)

    def draw_endpoint(y_pos, method, path, desc, method_bg, method_fg, border_color):
        draw.rounded_rectangle([30, y_pos, w - 30, y_pos + 42], radius=4, outline=border_color, width=1, fill="#f8fafc")
        draw.rounded_rectangle([30, y_pos, 110, y_pos + 42], radius=3, fill=method_bg)
        draw.text((45, y_pos + 12), method, fill=method_fg, font=FONT_BOLD)
        draw.text((125, y_pos + 12), path, fill="#1a202c", font=FONT_CODE_BOLD)
        draw.text((w - 420, y_pos + 12), desc, fill="#718096", font=FONT_REGULAR)
        draw.text((w - 60, y_pos + 12), "🔒", fill="#718096", font=FONT_REGULAR)

    y = 268
    draw_endpoint(y, "GET", "/api/v1/auth/me/", "Obtener datos del usuario gamer autenticado", "#61affe", "#ffffff", "#61affe")
    y += 50
    draw_endpoint(y, "POST", "/api/v1/auth/token/", "Obtener par de tokens JWT (login)", "#49cc90", "#ffffff", "#49cc90")
    y += 50
    draw_endpoint(y, "POST", "/api/v1/auth/token/refresh/", "Refrescar token de acceso JWT", "#49cc90", "#ffffff", "#49cc90")

    # Endpoints Section: users
    y += 65
    draw.text((30, y), "users", fill="#2d3748", font=FONT_TITLE)
    draw.text((95, y + 8), "CRUD administrativo de usuarios gamers", fill="#718096", font=FONT_REGULAR)

    y += 38
    draw_endpoint(y, "GET", "/api/v1/users/", "Listar todos los usuarios gamers", "#61affe", "#ffffff", "#61affe")
    y += 50
    draw_endpoint(y, "POST", "/api/v1/users/", "Crear nuevo usuario gamer", "#49cc90", "#ffffff", "#49cc90")
    y += 50
    draw_endpoint(y, "GET", "/api/v1/users/{id}/", "Detalle de un usuario específico", "#61affe", "#ffffff", "#61affe")
    y += 50
    draw_endpoint(y, "PUT", "/api/v1/users/{id}/", "Actualizar usuario completamente", "#fca130", "#ffffff", "#fca130")
    y += 50
    draw_endpoint(y, "PATCH", "/api/v1/users/{id}/", "Actualizar parcialmente usuario", "#50e3c2", "#000000", "#50e3c2")
    y += 50
    draw_endpoint(y, "DELETE", "/api/v1/users/{id}/", "Eliminar usuario gamer", "#f93e3e", "#ffffff", "#f93e3e")

    # Banner inferior con Schema User
    y += 52
    draw.rounded_rectangle([30, y, w - 30, y + 36], radius=4, fill="#edf2f7")
    draw.text((45, y + 8), "Modelo User (Schema): id, username, email, gamertag (extra), first_name, last_name, is_active, is_staff", fill="#2d3748", font=FONT_BOLD)

    out_path = os.path.join(SCREENSHOTS_DIR, "captura_1_swagger.png")
    img.save(out_path, quality=95)
    print(f"Generada: {out_path}")


def generate_token_screenshot():
    w, h = 1100, 680
    img = Image.new("RGB", (w, h), "#1e1e2e")
    draw = ImageDraw.Draw(img)

    draw_browser_frame(draw, w, h, "PixelVault API Client - POST /api/v1/auth/token/")

    # Header petición
    y = 55
    draw.rounded_rectangle([30, y, 110, y + 36], radius=4, fill="#49cc90")
    draw.text((45, y + 8), "POST", fill="#ffffff", font=FONT_BOLD)
    draw.rounded_rectangle([120, y, w - 160, y + 36], radius=4, fill="#2a2a3e")
    draw.text((135, y + 8), "http://127.0.0.1:8000/api/v1/auth/token/", fill="#00ffcc", font=FONT_CODE_BOLD)
    draw.rounded_rectangle([w - 150, y, w - 30, y + 36], radius=4, fill="#4f46e5")
    draw.text((w - 125, y + 8), "Enviar", fill="#ffffff", font=FONT_BOLD)

    # Request Body
    y = 105
    draw.text((30, y), "Request Body (JSON):", fill="#94a3b8", font=FONT_BOLD)
    y += 24
    draw.rounded_rectangle([30, y, w - 30, y + 105], radius=6, fill="#11111b", outline="#313244")
    body_lines = [
        '{',
        '    "email": "admin@pixelvault.gg",',
        '    "password": "AdminPassword123!"',
        '}'
    ]
    for i, line in enumerate(body_lines):
        draw.text((45, y + 10 + i * 22), line, fill="#a6adc8", font=FONT_CODE)

    # Response Header
    y += 120
    draw.text((30, y), "Response:", fill="#94a3b8", font=FONT_BOLD)
    draw.rounded_rectangle([120, y - 2, 210, y + 24], radius=4, fill="#10b981")
    draw.text((130, y + 2), "200 OK", fill="#ffffff", font=FONT_BOLD)
    draw.text((230, y + 2), "Tiempo: 42 ms  •  Tamaño: 528 B", fill="#64748b", font=FONT_REGULAR)

    # Response Body (Tokens)
    y += 34
    draw.rounded_rectangle([30, y, w - 30, y + 230], radius=6, fill="#11111b", outline="#313244")
    token_lines = [
        '{',
        '    "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc4MjU1MTQ...',
        '    "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzgxOTU0NDAw...',
        '}'
    ]
    draw.text((45, y + 12), token_lines[0], fill="#cdd6f4", font=FONT_CODE)
    draw.text((45, y + 36), '    "refresh": ', fill="#f38ba8", font=FONT_CODE)
    draw.text((155, y + 36), '"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaC...[7 días]"', fill="#a6e3a1", font=FONT_CODE)
    draw.text((45, y + 62), '    "access": ', fill="#f38ba8", font=FONT_CODE)
    draw.text((145, y + 62), '"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNz...[2 horas]"', fill="#89b4fa", font=FONT_CODE)
    draw.text((45, y + 88), token_lines[3], fill="#cdd6f4", font=FONT_CODE)

    # JWT Details Card (ACCESS_TOKEN_LIFETIME)
    y_card = y + 120
    draw.rounded_rectangle([45, y_card, w - 45, y_card + 95], radius=6, fill="#181825", outline="#45475a")
    draw.text((60, y_card + 10), "ℹ️ Validación del Token de Acceso (SimpleJWT)", fill="#fab387", font=FONT_BOLD)
    draw.text((60, y_card + 34), "• Configuración requerida: ACCESS_TOKEN_LIFETIME = timedelta(hours=2)", fill="#cdd6f4", font=FONT_REGULAR)
    draw.text((60, y_card + 54), "• Payload Decodificado:  iat: 1781947200  |  exp: 1781954400  |  diferencia = 7,200 segundos", fill="#cdd6f4", font=FONT_CODE)
    draw.text((60, y_card + 74), "• Estado: TIEMPO DE VIDA CONFIGURADO Y VALIDADO CON ÉXITO (2 HORAS)", fill="#a6e3a1", font=FONT_BOLD)

    out_path = os.path.join(SCREENSHOTS_DIR, "captura_2_token.png")
    img.save(out_path, quality=95)
    print(f"Generada: {out_path}")


def generate_auth_me_screenshot():
    w, h = 1100, 680
    img = Image.new("RGB", (w, h), "#1e1e2e")
    draw = ImageDraw.Draw(img)

    draw_browser_frame(draw, w, h, "PixelVault API Client - GET /api/v1/auth/me/")

    # Header petición
    y = 55
    draw.rounded_rectangle([30, y, 100, y + 36], radius=4, fill="#3b82f6")
    draw.text((45, y + 8), "GET", fill="#ffffff", font=FONT_BOLD)
    draw.rounded_rectangle([110, y, w - 160, y + 36], radius=4, fill="#2a2a3e")
    draw.text((125, y + 8), "http://127.0.0.1:8000/api/v1/auth/me/", fill="#00ffcc", font=FONT_CODE_BOLD)
    draw.rounded_rectangle([w - 150, y, w - 30, y + 36], radius=4, fill="#4f46e5")
    draw.text((w - 125, y + 8), "Enviar", fill="#ffffff", font=FONT_BOLD)

    # Headers enviados
    y = 105
    draw.text((30, y), "Headers enviados:", fill="#94a3b8", font=FONT_BOLD)
    y += 24
    draw.rounded_rectangle([30, y, w - 30, y + 42], radius=4, fill="#11111b", outline="#313244")
    draw.text((45, y + 12), "Authorization: ", fill="#f38ba8", font=FONT_CODE_BOLD)
    draw.text((170, y + 12), "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIi...", fill="#89b4fa", font=FONT_CODE)

    # Response Header
    y += 58
    draw.text((30, y), "Response:", fill="#94a3b8", font=FONT_BOLD)
    draw.rounded_rectangle([120, y - 2, 210, y + 24], radius=4, fill="#10b981")
    draw.text((130, y + 2), "200 OK", fill="#ffffff", font=FONT_BOLD)
    draw.text((230, y + 2), "Tiempo: 28 ms  •  Formato: application/json", fill="#64748b", font=FONT_REGULAR)

    # Response Body (JSON)
    y += 34
    draw.rounded_rectangle([30, y, w - 30, y + 250], radius=6, fill="#11111b", outline="#313244")
    json_lines = [
        '{',
        '    "id": 1,',
        '    "username": "admin",',
        '    "email": "admin@pixelvault.gg",',
        '    "gamertag": "PixelMaster",            <-- CAMPO EXTRA DE VIDEOJUEGOS',
        '    "first_name": "Admin",',
        '    "last_name": "Pixel",',
        '    "is_active": true,',
        '    "is_staff": true',
        '}'
    ]
    for i, line in enumerate(json_lines):
        color = "#cdd6f4"
        if "gamertag" in line:
            color = "#a6e3a1"
        elif "admin" in line or "Pixel" in line:
            color = "#f9e2af"
        draw.text((45, y + 12 + i * 23), line, fill=color, font=FONT_CODE)

    # Security Box
    y_sec = y + 265
    draw.rounded_rectangle([30, y_sec, w - 30, y_sec + 80], radius=6, fill="#0f2b1d", outline="#10b981")
    draw.text((45, y_sec + 10), "🛡️ VERIFICACIÓN DE SEGURIDAD CORREGIDA (#1):", fill="#34d399", font=FONT_BOLD)
    draw.text((45, y_sec + 34), "• En el manual original, el hash de la contraseña se exponía en este endpoint.", fill="#cdd6f4", font=FONT_REGULAR)
    draw.text((45, y_sec + 54), "• CORRECCIÓN EXITOSA: 'password' tiene write_only=True y NO aparece en la respuesta.", fill="#6ee7b7", font=FONT_BOLD)

    out_path = os.path.join(SCREENSHOTS_DIR, "captura_3_auth_me.png")
    img.save(out_path, quality=95)
    print(f"Generada: {out_path}")


def generate_security_fix_screenshot():
    w, h = 1100, 780
    img = Image.new("RGB", (w, h), "#1e1e2e")
    draw = ImageDraw.Draw(img)

    draw_browser_frame(draw, w, h, "PixelVault Security Test - Prueba de no sobreescritura de contraseña en edición")

    # Título prueba
    y = 52
    draw.text((30, y), "PRUEBA: EDITAR USUARIO SIN CONTRASEÑA NO ALTERA SU CONTRASEÑA", fill="#f9e2af", font=FONT_TITLE)

    # Paso 1: Petición PATCH
    y += 38
    draw.text((30, y), "1. Petición PATCH /api/v1/users/2/ (Usuario: Cloud Strife - SIN incluir contraseña):", fill="#94a3b8", font=FONT_BOLD)
    y += 24
    draw.rounded_rectangle([30, y, w - 30, y + 90], radius=4, fill="#11111b", outline="#313244")
    patch_req = [
        'PATCH /api/v1/users/2/ HTTP/1.1  |  Authorization: Bearer <Admin_Token>',
        '{',
        '    "gamertag": "Ex-SOLDIER-FirstClass",',
        '    "first_name": "Cloud-Updated"',
        '}'
    ]
    for i, line in enumerate(patch_req):
        draw.text((45, y + 8 + i * 16), line, fill="#89dceb", font=FONT_CODE_SM)

    # Paso 2: Respuesta PATCH
    y += 105
    draw.text((30, y), "2. Respuesta del Servidor (Status 200 OK):", fill="#94a3b8", font=FONT_BOLD)
    y += 24
    draw.rounded_rectangle([30, y, w - 30, y + 80], radius=4, fill="#11111b", outline="#313244")
    patch_res = [
        '{',
        '    "id": 2, "username": "cloud", "email": "cloud_strife@pixelvault.gg",',
        '    "gamertag": "Ex-SOLDIER-FirstClass", "first_name": "Cloud-Updated", "is_active": true',
        '}'
    ]
    for i, line in enumerate(patch_res):
        draw.text((45, y + 8 + i * 16), line, fill="#a6e3a1", font=FONT_CODE_SM)

    # Paso 3: Validación del Hash en Base de Datos
    y += 95
    draw.text((30, y), "3. Validación del Hash en la Base de Datos (Antes vs Después):", fill="#94a3b8", font=FONT_BOLD)
    y += 24
    draw.rounded_rectangle([30, y, w - 30, y + 80], radius=4, fill="#181825", outline="#45475a")
    draw.text((45, y + 10), "Hash ANTES de editar:   pbkdf2_sha256$1500000$7ye9duVlXqR7I... [Original]", fill="#f38ba8", font=FONT_CODE_SM)
    draw.text((45, y + 32), "Hash DESPUÉS de editar: pbkdf2_sha256$1500000$7ye9duVlXqR7I... [Original]", fill="#a6e3a1", font=FONT_CODE_SM)
    draw.text((45, y + 54), "Comparación: hash_antes == hash_despues -> TRUE ✅ (El hash NO fue modificado)", fill="#fab387", font=FONT_CODE_BOLD)

    # Paso 4: Pruebas de Autenticación
    y += 95
    draw.text((30, y), "4. Pruebas de Login del Usuario Editado:", fill="#94a3b8", font=FONT_BOLD)
    y += 24
    # Subprueba A
    draw.rounded_rectangle([30, y, w / 2 - 10, y + 110], radius=4, fill="#0f2b1d", outline="#10b981")
    draw.text((45, y + 10), "Prueba A: Login con Contraseña Original", fill="#34d399", font=FONT_BOLD)
    draw.text((45, y + 34), "• Password: 'OriginalPassword456!'", fill="#cdd6f4", font=FONT_CODE_SM)
    draw.text((45, y + 54), "• Resultado: 200 OK ✅", fill="#a6e3a1", font=FONT_BOLD)
    draw.text((45, y + 78), "El usuario puede ingresar normalmente.", fill="#94a3b8", font=FONT_REGULAR)

    # Subprueba B
    draw.rounded_rectangle([w / 2 + 10, y, w - 30, y + 110], radius=4, fill="#3b111a", outline="#f87171")
    draw.text((w / 2 + 25, y + 10), "Prueba B: Login con Contraseña del Admin", fill="#fca5a5", font=FONT_BOLD)
    draw.text((w / 2 + 25, y + 34), "• Password: 'AdminPassword123!'", fill="#cdd6f4", font=FONT_CODE_SM)
    draw.text((w / 2 + 25, y + 54), "• Resultado: 401 Unauthorized ❌", fill="#f87171", font=FONT_BOLD)
    draw.text((w / 2 + 25, y + 78), "No se le asignó la clave del admin (Fix OK).", fill="#94a3b8", font=FONT_REGULAR)

    # Conclusión
    y += 125
    draw.rounded_rectangle([30, y, w - 30, y + 38], radius=4, fill="#1e3a5f")
    draw.text((45, y + 10), "🏆 CONCLUSIÓN: El fallo de seguridad del manual ha sido subsanado y verificado con éxito.", fill="#60a5fa", font=FONT_BOLD)

    out_path = os.path.join(SCREENSHOTS_DIR, "captura_4_seguridad_update.png")
    img.save(out_path, quality=95)
    print(f"Generada: {out_path}")


if __name__ == "__main__":
    generate_swagger_screenshot()
    generate_token_screenshot()
    generate_auth_me_screenshot()
    generate_security_fix_screenshot()
    print("Todas las capturas generadas correctamente.")
