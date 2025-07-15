from django.urls import path
from prestamos.views import PrestamosList, PrestamosDetail


urlpatterns = [
    path('prestamos/', PrestamosList.as_view(), name='prestamos-list'),
    path('prestamos/<int:pk>/', PrestamosDetail.as_view(), name='prestamos-detail'),
]