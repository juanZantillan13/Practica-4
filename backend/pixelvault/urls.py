"""
URL configuration for pixelvault project.
Video Game Backend Platform API Documentation & Routes.
"""

from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="PixelVault Gaming API",
        default_version='v1',
        description=(
            "API RESTful para la plataforma de videojuegos y comunidad PixelVault.\n\n"
            "Incluye autenticación mediante JWT (JSON Web Tokens), gestión completa (CRUD) "
            "de usuarios gamers con campo personalizado 'gamertag', consulta de datos de perfil "
            "y correcciones de seguridad avanzadas."
        ),
        terms_of_service="https://www.pixelvault.gg/terms/",
        contact=openapi.Contact(email="admin@pixelvault.gg"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
