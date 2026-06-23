from django.urls import path
from . import views
from .views import registro_bencina

urlpatterns = [
    path('', views.home, name='home'),
    path('registro/', registro_bencina, name='registro_bencina'),
]