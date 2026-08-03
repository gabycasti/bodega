from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('gestion_listado/', views.gestion_listado, name='gestion_listado'),
    path('permiso_circulacion/', views.permiso_circulacion, name='permiso_circulacion'),
   
]

