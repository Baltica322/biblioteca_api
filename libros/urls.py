from django.urls import path
from libros.views import LibrosList, LibrosDetail
from libros.views import SucursalesList, SucursalesDetail
from libros.views import EjemplaresList, EjemplaresDetail

urlpatterns = [
    path('libros/', LibrosList.as_view(), name='libros-list'),
    path('libros/<int:pk>/', LibrosDetail.as_view(), name='libros-detail'),
    path('sucursales/', SucursalesList.as_view(), name='sucursales-list'),
    path('sucursales/<int:pk>/', SucursalesDetail.as_view(), name='sucursales-detail'),
    path('ejemplares/', EjemplaresList.as_view(), name='ejemplares-list'),
    path('ejemplares/<int:pk>/', EjemplaresDetail.as_view(), name='ejemplares-detail'),
]