from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('regular', 'Usuario regular'),
        ('bibliotecario', 'Bibliotecario'),
        ('admin', 'Administrador'),
    )
    rol = models.CharField(max_length=20, choices=ROLES, default='regular')

    def __str__ (self):
        return f"{self.username} ({self.rol})"