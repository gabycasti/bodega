from django.urls import path
from . import views

urlpatterns = [
    path("crear_documento/", views.crear_documento, name="crear_documento"),
    path('listado_documento/', views.listado_documento, name='listado_documento'),
]