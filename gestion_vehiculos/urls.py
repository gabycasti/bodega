from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('gestion_listado/', views.gestion_listado, name='gestion_listado'),
    path('permiso_circulacion/', views.permiso_circulacion, name='permiso_circulacion'),
    path('editar_permiso_circulacion/<int:id>/',views.editar_permiso_circulacion,name='editar_permiso_circulacion'),
    path('eliminar_permiso_circulacion/<int:id>/',views.eliminar_permiso_circulacion,name='eliminar_permiso_circulacion'),
   
]

