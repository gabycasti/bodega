from django.urls import path
from . import views


urlpatterns = [
    path('listado/', views.empleado_listado, name='empleado_listado'),

    path('registro/', views.registro_empleado, name='registro_empleado'),
]
