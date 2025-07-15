from rest_framework.permissions import BasePermission

# Permite solo al usuario con rol 'admin'
class EsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'admin'


# Permite solo al usuario con rol 'bibliotecario'
class EsBibliotecario(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'bibliotecario'


# Permite solo al usuario con rol 'regular'
class EsRegular(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.rol == 'regular'


# Permite si el usuario es admin o bibliotecario
class EsAdminOBibliotecario(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and 
            request.user.rol in ['admin', 'bibliotecario']
        )


# Permite si el usuario es admin, bibliotecario o el dueño del objeto
class EsAdminOBibliotecarioODueno(BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated and (
                request.user.rol in ['admin', 'bibliotecario'] or 
                obj == request.user
            )
        )
