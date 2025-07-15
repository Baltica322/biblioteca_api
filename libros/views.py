from django.shortcuts import render
from libros.serializers import LibrosSerializer, EjemplaresSerializer, SucursalesSerializer
from libros.models import Libro, Ejemplar, Sucursal
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import IsAuthenticated
from libros.permisos import EsAdminOBibliotecario, EsBibliotecario, EsAdmin

class LibrosList(APIView):
    permission_classes = [IsAuthenticated, EsBibliotecario]

    def get(self, request):
        libros = Libro.objects.all()
        serializer = LibrosSerializer(libros, many=True)
        return Response(serializer.data)

    def post(self, request):
        isbn = request.data.get("isbn")
        if Libro.objects.filter(isbn=isbn).exists():
            return Response({"error": "Ya existe un libro con ese ISBN."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LibrosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LibrosDetail(APIView):
    permission_classes = [IsAuthenticated, EsBibliotecario]

    def get_object(self, pk):
        try:
            return Libro.objects.get(pk=pk)
        except Libro.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        libro = self.get_object(pk)
        serializer = LibrosSerializer(libro)
        return Response(serializer.data)

    def put(self, request, pk):
        libro = self.get_object(pk)
        isbn = request.data.get("isbn")
        if isbn and Libro.objects.filter(isbn=isbn).exclude(pk=pk).exists():
            return Response({"error": "Ya existe otro libro con ese ISBN."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LibrosSerializer(libro, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        libro = self.get_object(pk)
        libro.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class SucursalesList(APIView):
    permission_classes = [IsAuthenticated, EsAdmin]

    def get(self, request):
        sucursales = Sucursal.objects.all()
        serializer = SucursalesSerializer(sucursales, many=True)
        return Response(serializer.data)

    def post(self, request):
        nombre = request.data.get("nombre")
        direccion = request.data.get("direccion")
        if Sucursal.objects.filter(nombre=nombre, direccion=direccion).exists():
            return Response({"error": "Ya existe una sucursal con ese nombre y dirección."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SucursalesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SucursalesDetail(APIView):
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_object(self, pk):
        try:
            return Sucursal.objects.get(pk=pk)
        except Sucursal.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        sucursal = self.get_object(pk)
        serializer = SucursalesSerializer(sucursal)
        return Response(serializer.data)

    def put(self, request, pk):
        sucursal = self.get_object(pk)
        nombre = request.data.get("nombre")
        direccion = request.data.get("direccion")
        if nombre and direccion and Sucursal.objects.filter(nombre=nombre, direccion=direccion).exclude(pk=pk).exists():
            return Response({"error": "Ya existe otra sucursal con ese nombre y dirección."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = SucursalesSerializer(sucursal, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        sucursal = self.get_object(pk)
        sucursal.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class EjemplaresList(APIView):
    permission_classes = [IsAuthenticated, EsAdminOBibliotecario]

    def get(self, request):
        ejemplares = Ejemplar.objects.all()
        serializer = EjemplaresSerializer(ejemplares, many=True)
        return Response(serializer.data)

    def post(self, request):
        codigo_barras = request.data.get("codigo_barras")
        libro_id = request.data.get("libro")
        sucursal_id = request.data.get("sucursal")

        if Ejemplar.objects.filter(codigo_barras=codigo_barras).exists():
            return Response({"error": "Ya existe un ejemplar con ese código de barras."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validar que libro y sucursal existan
        if not Libro.objects.filter(pk=libro_id).exists():
            return Response({"error": "El libro especificado no existe."}, status=status.HTTP_400_BAD_REQUEST)
        if not Sucursal.objects.filter(pk=sucursal_id).exists():
            return Response({"error": "La sucursal especificada no existe."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EjemplaresSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EjemplaresDetail(APIView):
    permission_classes = [IsAuthenticated, EsAdminOBibliotecario]

    def get_object(self, pk):
        try:
            return Ejemplar.objects.get(pk=pk)
        except Ejemplar.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        ejemplar = self.get_object(pk)
        serializer = EjemplaresSerializer(ejemplar)
        return Response(serializer.data)

    def put(self, request, pk):
        ejemplar = self.get_object(pk)
        codigo_barras = request.data.get("codigo_barras")
        libro_id = request.data.get("libro")
        sucursal_id = request.data.get("sucursal")

        if codigo_barras and Ejemplar.objects.filter(codigo_barras=codigo_barras).exclude(pk=pk).exists():
            return Response({"error": "Ya existe otro ejemplar con ese código de barras."}, status=status.HTTP_400_BAD_REQUEST)
        if libro_id and not Libro.objects.filter(pk=libro_id).exists():
            return Response({"error": "El libro especificado no existe."}, status=status.HTTP_400_BAD_REQUEST)
        if sucursal_id and not Sucursal.objects.filter(pk=sucursal_id).exists():
            return Response({"error": "La sucursal especificada no existe."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = EjemplaresSerializer(ejemplar, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        ejemplar = self.get_object(pk)
        ejemplar.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
