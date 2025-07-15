from django.urls import path
from reservas.views import ReservasList, ReservasDetail


urlpatterns = [
    path('reservas/', ReservasList.as_view(), name='reservas-list'),
    path('reservas/<int:pk>/', ReservasDetail.as_view(), name='reservas-detail'),
]