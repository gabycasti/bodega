from django.urls import path
from . import views


urlpatterns = [
    path('listado/', views.empleado_listado, name='empleado_listado'),

    path('registro/', views.registro_empleado, name='registro_empleado'),

    path('editar/<int:id>/', views.editar_empleado, name='editar_empleado'),

       path(
        'cambiar_estado/<int:id>/',
        views.cambiar_estado_empleado,
        name='cambiar_estado_empleado'
    ),

]
