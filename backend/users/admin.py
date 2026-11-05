from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from users.models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Configuración del modelo User en el Django Admin de PixelVault.
    Muestra explícitamente el campo extra 'gamertag' tanto en la lista
    como en los formularios de edición y creación.
    """
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Información Personal y Gamer', {'fields': ('first_name', 'last_name', 'username', 'gamertag')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'gamertag', 'password', 'is_staff', 'is_active'),
        }),
    )
    list_display = ('id', 'email', 'username', 'gamertag', 'is_staff', 'is_active')
    search_fields = ('email', 'username', 'gamertag')
    ordering = ('id',)
