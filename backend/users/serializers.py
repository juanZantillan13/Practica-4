from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo User en PixelVault.
    
    CORRECCIÓN DE SEGURIDAD 1:
    - Se configura 'password' como 'write_only': True.
    - Esto garantiza que el hash de la contraseña NUNCA se exponga en las
      respuestas de la API (ni en el listado de usuarios ni en /auth/me/).
      
    CORRECCIÓN DE SEGURIDAD 2:
    - En el método update(), si no se envía una contraseña, la existente
      se mantiene intacta. En ningún caso se sobreescribe con la del usuario que
      realiza la petición.
    """
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'gamertag',
            'first_name',
            'last_name',
            'password',
            'is_active',
            'is_staff'
        ]
        extra_kwargs = {
            'password': {
                'write_only': True,
                'required': False
            }
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user

    def update(self, instance, validated_data):
        # Si la petición no incluye contraseña, pop devuelve None y no se modifica
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user
