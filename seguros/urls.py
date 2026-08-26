from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('seguro_listado/', views.seguro_listado, name='seguro_listado'),
    path('seguro/', views.seguro, name='seguro'),
    path('editar/<int:id>/', views.editar_seguro, name='editar_seguro'),
    path('eliminar/<int:id>/', views.eliminar_seguro, name='eliminar_seguro'),
]