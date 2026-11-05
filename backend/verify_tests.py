import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pixelvault.settings')
django.setup()

from django.test import Client
from users.models import User
from rest_framework_simplejwt.tokens import AccessToken

client = Client()

print("=" * 60)
print("EJECUTANDO SUITE DE PRUEBAS AUTOMATIZADAS - PIXELVAULT API")
print("=" * 60)

# TEST 1: Login JWT
print("\n[TEST 1] Login JWT (/api/v1/auth/token/):")
res_login = client.post(
    '/api/v1/auth/token/',
    data=json.dumps({
        'email': 'admin@pixelvault.gg',
        'password': 'AdminPassword123!'
    }),
    content_type='application/json'
)
assert res_login.status_code == 200, f"Error en login: {res_login.status_code} {res_login.content}"
login_data = res_login.json()
print("  -> Status code: 200 OK")
print("  -> Claves recibidas:", list(login_data.keys()))
access_token = login_data['access']

token_obj = AccessToken(access_token)
lifetime = token_obj['exp'] - token_obj['iat']
print(f"  -> ACCESS_TOKEN_LIFETIME: {lifetime} segundos ({lifetime / 3600:.1f} horas)")
assert lifetime == 7200, f"ACCESS_TOKEN_LIFETIME esperado 7200s (2h), obtenido {lifetime}s"

# TEST 2: Endpoint datos personales (/api/v1/auth/me/)
print("\n[TEST 2] Endpoint datos personales (/api/v1/auth/me/) y Seguridad de Contraseña:")
res_me = client.get('/api/v1/auth/me/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
assert res_me.status_code == 200, f"Error en /auth/me/: {res_me.status_code}"
me_data = res_me.json()
print("  -> Status code: 200 OK")
print("  -> Datos devueltos:", json.dumps(me_data, indent=2))
print("  -> ¿Contraseña presente en respuesta?:", 'password' in me_data)
assert 'password' not in me_data, "VULNERABILIDAD DETECTADA: ¡El hash de contraseña apareció en la respuesta!"
assert 'gamertag' in me_data, "ERROR: El campo extra 'gamertag' no está en la respuesta"
print("  -> ÉXITO: El hash de la contraseña NO se expone y el campo 'gamertag' está presente.")

# TEST 3: Listado de usuarios (/api/v1/users/)
print("\n[TEST 3] Listado CRUD (/api/v1/users/):")
res_users = client.get('/api/v1/users/', HTTP_AUTHORIZATION=f'Bearer {access_token}')
assert res_users.status_code == 200, f"Error en /users/: {res_users.status_code}"
users_list = res_users.json()
print(f"  -> Total usuarios encontrados: {len(users_list)}")
for u in users_list:
    assert 'password' not in u, f"VULNERABILIDAD: Password presente en {u['email']}"
print("  -> ÉXITO: Ningún usuario en el listado expone su hash de contraseña.")

# TEST 4: Prueba de corrección del fallo del manual (editar sin contraseña)
print("\n[TEST 4] Prueba de corrección del fallo del manual (Editar sin contraseña):")
cloud = User.objects.get(email='cloud_strife@pixelvault.gg')
hash_antes = cloud.password
print(f"  -> Hash de Cloud ANTES de editar: {hash_antes[:35]}...")

res_patch = client.patch(
    f'/api/v1/users/{cloud.id}/',
    data=json.dumps({
        'gamertag': 'Ex-SOLDIER-FirstClass',
        'first_name': 'Cloud-Updated'
    }),
    content_type='application/json',
    HTTP_AUTHORIZATION=f'Bearer {access_token}'
)
assert res_patch.status_code == 200, f"Error en PATCH: {res_patch.status_code} {res_patch.content}"
patch_data = res_patch.json()
print("  -> Respuesta de PATCH:", json.dumps(patch_data, indent=2))
assert 'password' not in patch_data

cloud.refresh_from_db()
hash_despues = cloud.password
print(f"  -> Hash de Cloud DESPUÉS de editar: {hash_despues[:35]}...")
print("  -> ¿El hash se mantuvo idéntico?:", hash_antes == hash_despues)
assert hash_antes == hash_despues, "VULNERABILIDAD DETECTADA: ¡El hash cambió indebidamente al editar sin contraseña!"

# Prueba de autenticación con contraseña original
res_cloud_login = client.post(
    '/api/v1/auth/token/',
    data=json.dumps({
        'email': 'cloud_strife@pixelvault.gg',
        'password': 'OriginalPassword456!'
    }),
    content_type='application/json'
)
assert res_cloud_login.status_code == 200, "ERROR: Cloud no pudo iniciar sesión con su contraseña original!"
print("  -> Login de Cloud con su contraseña original: 200 OK (Inicio de sesión exitoso)")

# Prueba de intento de autenticación con la contraseña del Admin
res_cloud_admin_pwd = client.post(
    '/api/v1/auth/token/',
    data=json.dumps({
        'email': 'cloud_strife@pixelvault.gg',
        'password': 'AdminPassword123!'
    }),
    content_type='application/json'
)
assert res_cloud_admin_pwd.status_code == 401, "VULNERABILIDAD: Cloud pudo loguearse con la contraseña del Admin!"
print("  -> Login de Cloud con contraseña del Admin: 401 Unauthorized (Rechazado correctamente)")

print("\n" + "=" * 60)
print(">>> TODAS LAS PRUEBAS Y CORRECCIONES PASARON AL 100% <<<")
print("=" * 60)
