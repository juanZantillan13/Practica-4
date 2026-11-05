from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer

class UserApiViewSet(ModelViewSet):
    """
    CRUD completo de usuarios gamers en PixelVault (solo accesible por administradores).
    
    CORRECCIÓN DE SEGURIDAD:
    En el manual original se encontraba la siguiente vulnerabilidad en partial_update:
        if "password" in request.data:
            request.data["password"] = make_password(request.data["password"])
        else:
            request.data["password"] = request.user.password  # <-- VULNERABILIDAD
            
    Dicho error asignaba la contraseña (hash) del administrador o usuario que realizaba
    la petición al usuario que estaba siendo editado, alterando y comprometiendo su acceso.
    
    Aquí la lógica se corrigió en UserSerializer y en el ViewSet:
    - Si se envía 'password', se actualiza y hashea de forma segura mediante set_password().
    - Si NO se envía 'password', la contraseña existente del usuario NO se toca en absoluto.
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')

    def partial_update(self, request, *args, **kwargs):
        # Aseguramos explícitamente que no se altere la contraseña si no viene en el payload
        kwargs['partial'] = True
        return super().partial_update(request, *args, **kwargs)


class UserView(APIView):
    """
    Endpoint para consultar los datos personales del usuario autenticado (/auth/me/).
    Requiere autenticación mediante token JWT (Bearer Token).
    
    CORRECCIÓN DE SEGURIDAD:
    Gracias a 'write_only: True' en UserSerializer, la contraseña (hash)
    NUNCA aparece en la respuesta de este endpoint ni en ningún otro.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
