from django.shortcuts import render
from reservas.serializers import ReservasSerializer
from reservas.models import Reserva
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from libros.models import Libro


# Vista para listar y crear estudiantes
class ReservasList(APIView):

    def get(self, request):
        reservas = Reserva.objects.all()
        serializer = ReservasSerializer(reservas, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        usuario = request.data.get("usuario")
        libro_id = request.data.get("libro")
        posicion = request.data.get("posicion_cola")

        # Validar que el libro exista
        try:
            libro_obj = Libro.objects.get(pk=libro_id)
        except Libro.DoesNotExist:
            return Response(
                {"error": "El libro no está disponible."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validar si el libro ya tiene esa posición en la cola
        if Reserva.objects.filter(libro=libro_id, posicion_cola=posicion).exists():
            return Response(
                {"error": f"El libro ya está reservado en la posición {posicion}."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validar si el usuario ya pidió ese libro (en cualquier posición)
        if Reserva.objects.filter(libro=libro_id, usuario=usuario).exists():
            return Response(
                {"error": "El usuario ya reservó este libro."},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ReservasSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReservasDetail(APIView):

    def get_object(self, pk):
        try:
            return Reserva.objects.get(pk=pk)
        except Reserva.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        reservas = self.get_object(pk)
        serializer = ReservasSerializer(reservas)
        return Response(serializer.data)

    def put(self, request, pk):
        reservas = self.get_object(pk)
        serializer = ReservasSerializer(reservas, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        reservas = self.get_object(pk)
        reservas.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)