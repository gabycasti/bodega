from django.urls import path
from . import views


urlpatterns = [
    path('listado/', views.vehiculo_listado, name='vehiculo_listado'),

    path('registro/', views.registro_vehiculo, name='registro_vehiculo'),
]
