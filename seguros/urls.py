from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('seguro_listado/', views.seguro_listado, name='seguro_listado'),
    path('seguro/', views.seguro, name='seguro'),
    #path('editar_permiso_circulacion/<int:id>/',views.editar_permiso_circulacion,name='editar_permiso_circulacion'),
   # path('eliminar_permiso_circulacion/<int:id>/',views.eliminar_permiso_circulacion,name='eliminar_permiso_circulacion'),
   
]

