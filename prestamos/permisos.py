from rest_framework import permissions

class EsBibliotecario(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'bibliotecario'
    
class EsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'admin'

class EsAdminOBibliotecario(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
            request.user.rol == 'admin' or request.user.rol == 'bibliotecario'
        ) 