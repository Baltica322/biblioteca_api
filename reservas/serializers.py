from rest_framework import serializers
from reservas.models import Reserva


class ReservasSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reserva
        fields = '__all__'