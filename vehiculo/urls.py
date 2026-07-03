from django.urls import path
from . import views


urlpatterns = [
    path('listado/', views.vehiculo_listado, name='vehiculo_listado'),

    path('registro/', views.registro_vehiculo, name='registro_vehiculo'),

    path('vehiculo/editar/<int:id>/', views.editar_vehiculo, name='editar_vehiculo'),

    path('vehiculos/estado/<int:id>/',views.cambiar_estado_vehiculo,name='cambiar_estado_vehiculo'),
]
