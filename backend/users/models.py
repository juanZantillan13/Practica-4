from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    Modelo de Usuario personalizado para la plataforma de videojuegos PixelVault.
    Utiliza el email como identificador principal (USERNAME_FIELD) e incluye
    el campo adicional 'gamertag' para la identidad gamer del usuario.
    """
    email = models.EmailField(unique=True, verbose_name="Correo electrónico")
    username = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre de usuario")
    gamertag = models.CharField(max_length=50, blank=True, null=True, verbose_name="Gamertag")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Usuario Gamer"
        verbose_name_plural = "Usuarios Gamers"

    def save(self, *args, **kwargs):
        if not self.username and self.email:
            self.username = self.email.split('@')[0]
        super().save(*args, **kwargs)

    def __str__(self):
        tag = f" [{self.gamertag}]" if self.gamertag else ""
        return f"{self.email}{tag}"
