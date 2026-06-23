from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('listado/', views.listado, name='bencina_listado'),
    path('eliminar/<int:id>/', views.eliminar_bencina, name='eliminar_bencina'),
    path('bencina/', include('formulario_bencina.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)