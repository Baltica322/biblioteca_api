from django.db import models

# Create your models here.
class Sucursal(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.TextField()
    telefono = models.CharField(max_length=20)
    horario = models.TextField()

    def str(self):
        return self.nombre


class Libro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=100)
    isbn = models.CharField(max_length=13, unique=True)
    genero = models.CharField(max_length=50)
    año_publicacion = models.DateField()
    descripcion = models.TextField()

    def str(self):
        return self.titulo


class Ejemplar(models.Model):
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    codigo_barras = models.CharField(max_length=30, unique=True)
    ESTADOS = [
        ('disponible', 'Disponible'),
        ('prestado', 'Prestado'),
        ('mantenimiento', 'En mantenimiento'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADOS, default='disponible')

    def str(self):
        return f"{self.codigo_barras} - {self.libro.titulo} ({self.estado})"