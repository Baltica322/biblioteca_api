from django.db import models
from django.utils import timezone

from usuarios.models import Usuario
from libros.models import Libro

class Reserva(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=[('en_espera', 'En espera'), ('activa', 'Activa'), ('expirada', 'Expirada')], default='en_espera')
    posicion_cola = models.IntegerField()

    def __str__(self):
        return f"Reserva de {self.usuario.username} por {self.libro.titulo} (Posición {self.posicion_cola})"