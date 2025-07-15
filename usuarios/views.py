from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.http import Http404
from usuarios.models import Usuario
from usuarios.serializers import UsuariosSerializer
from usuarios.permisos import EsAdmin

class UsuariosList(APIView):
    permission_classes = [IsAuthenticated, EsAdmin]  # Solo admins pueden ver todos

    def get(self, request):
        usuarios = Usuario.objects.all()
        serializer = UsuariosSerializer(usuarios, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        # Aquí puedes permitir que se registre cualquier usuario
        serializer = UsuariosSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuariosDetail(APIView):
    permission_classes = [IsAuthenticated, EsAdmin]

    def get_object(self, pk):
        try:
            return Usuario.objects.get(pk=pk)
        except Usuario.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        usuario = self.get_object(pk)
        # Solo el propio usuario, admin o bibliotecario pueden verlo
        if request.user != usuario and request.user.rol not in ['admin', 'bibliotecario']:
            return Response({'detail': 'No autorizado'}, status=403)
        serializer = UsuariosSerializer(usuario)
        return Response(serializer.data)

    def put(self, request, pk):
        usuario = self.get_object(pk)
        if request.user != usuario and request.user.rol != 'admin':
            return Response({'detail': 'Solo puedes editar tu perfil o debes ser admin'}, status=403)
        serializer = UsuariosSerializer(usuario, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        usuario = self.get_object(pk)
        if request.user.rol != 'admin':
            return Response({'detail': 'Solo un administrador puede eliminar usuarios'}, status=403)
        usuario.delete()
        return Response(status=204)
