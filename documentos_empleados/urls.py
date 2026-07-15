from django.urls import path
from . import views

urlpatterns = [
    path("crear_documento/", views.crear_documento, name="crear_documento"),
    path('listado_documentos/', views.listado_documentos, name='listado_documentos'),
    path("editar_documento/<int:id>/", views.editar_documento, name="editar_documento"),
]