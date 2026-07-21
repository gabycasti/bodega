from django.urls import path
from . import views

urlpatterns = [
    path("crear_documento/", views.crear_documento, name="crear_documento"),
    path('listado_documentos/', views.listado_documentos, name='listado_documentos'),
    path('listado_francisco/', views.listado_francisco, name='listado_francisco'),
    path('listado_viel/', views.listado_viel, name='listado_viel'),
    path("editar_documento/<int:id>/", views.editar_documento, name="editar_documento"),
]