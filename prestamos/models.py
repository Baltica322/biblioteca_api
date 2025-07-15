from django.db import models
from django.utils import timezone
from datetime import timedelta

from usuarios.models import Usuario
from libros.models import Ejemplar

def default_fecha_devolucion():
    return timezone.now().date() + timedelta(days=14)

class Prestamo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    ejemplar = models.ForeignKey(Ejemplar, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField(default=timezone.now)
    fecha_devolucion = models.DateField(default=default_fecha_devolucion)
    estado = models.CharField(max_length=20, choices=[('activo', 'Activo'), ('devuelto', 'Devuelto')], default='activo')
    multa = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def calcular_multa(self):
        if self.estado == 'activo' and timezone.now().date() > self.fecha_devolucion:
            dias_atraso = (timezone.now().date() - self.fecha_devolucion).days
            return dias_atraso * 500  
        return 0

    def __str__(self):
        return f"Préstamo: {self.usuario.username} - {self.ejemplar.codigo_barras}"