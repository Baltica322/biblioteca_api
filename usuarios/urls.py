from django.urls import path
from usuarios.views import UsuariosList, UsuariosDetail


urlpatterns = [
    path('usuarios/', UsuariosList.as_view(), name='usuarios-list'),
    path('usuarios/<int:pk>/', UsuariosDetail.as_view(), name='usuarios-detail'),
]