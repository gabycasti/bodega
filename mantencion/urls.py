from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('listado_mantencion/', views.listado_mantencion, name='listado_mantencion'),
    path('agregar_mantencion/', views.agregar_mantencion, name='agregar_mantencion'),
    path('editar_mantencion/<int:id>/',views.editar_mantencion,name='editar_mantencion'),
    path('eliminar_mantencion/<int:id>/',views.eliminar_mantencion,name='eliminar_mantencion'),
   
]
