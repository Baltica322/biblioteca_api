from django.shortcuts import render
from prestamos.serializers import PrestamosSerializer
from prestamos.models import Prestamo
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from prestamos.permisos import EsAdminOBibliotecario
from libros.models import Ejemplar

class PrestamosList(APIView):
    permission_classes = [IsAuthenticated, EsAdminOBibliotecario]

    def get(self, request):
        prestamos = Prestamo.objects.all()
        serializer = PrestamosSerializer(prestamos, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        ejemplar_id = request.data.get("ejemplar")

        # Validar si el ejemplar existe
        if not Ejemplar.objects.filter(id=ejemplar_id).exists():
            return Response(
                {"error": "El ejemplar indicado no existe."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar si el ejemplar ya tiene un préstamo activo
        if Prestamo.objects.filter(ejemplar_id=ejemplar_id, estado='activo').exists():
            return Response(
                {"error": "Este ejemplar ya está prestado y no está disponible."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar si el ejemplar está en mantenimiento
        ejemplar = Ejemplar.objects.get(id=ejemplar_id)
        if ejemplar.estado == 'mantenimiento':
            return Response(
                {"error": "Este ejemplar está en mantenimiento y no puede ser prestado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = PrestamosSerializer(data=request.data)
        if serializer.is_valid():
            prestamo = serializer.save()

            # Marcar ejemplar como prestado
            ejemplar.estado = 'prestado'
            ejemplar.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PrestamosDetail(APIView):
    permission_classes = [IsAuthenticated, EsAdminOBibliotecario]

    def get_object(self, pk):
        try:
            return Prestamo.objects.get(pk=pk)
        except Prestamo.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        prestamos = self.get_object(pk)
        serializer = PrestamosSerializer(prestamos)
        return Response(serializer.data)

    def put(self, request, pk):
        prestamos = self.get_object(pk)
        serializer = PrestamosSerializer(prestamos, data=request.data)
        if serializer.is_valid():
            prestamo_actualizado = serializer.save()

            # Si el préstamo fue devuelto, liberar ejemplar
            if prestamo_actualizado.estado == 'devuelto':
                ejemplar = prestamo_actualizado.ejemplar
                ejemplar.estado = 'disponible'
                ejemplar.save()

            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        prestamos = self.get_object(pk)
        
        # Liberar ejemplar si aún está prestado
        if prestamos.estado == 'activo':
            ejemplar = prestamos.ejemplar
            ejemplar.estado = 'disponible'
            ejemplar.save()

        prestamos.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
