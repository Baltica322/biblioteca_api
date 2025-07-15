from rest_framework import serializers
from libros.models import Libro
from libros.models import Sucursal
from libros.models import Ejemplar

class LibrosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Libro
        fields = '__all__'

class SucursalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sucursal
        fields = '__all__'

class EjemplaresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ejemplar
        fields = '__all__'