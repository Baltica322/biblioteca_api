from rest_framework import serializers
from prestamos.models import Prestamo


class PrestamosSerializer(serializers.ModelSerializer):

    class Meta:
        model = Prestamo
        fields = '__all__'

