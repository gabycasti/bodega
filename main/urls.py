from django.urls import path
from .views import dashboard
from django.urls import path, include
from django.views.generic import RedirectView
from main import views
from django.contrib.auth import views as auth_views



urlpatterns = [
    # LOGIN
 
    # LOGIN
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # DASHBOARD PROTEGIDO
    path('', views.dashboard, name='dashboard'),
   

    # USUARIOS
    #path('crear_usuario/', views.crear_usuario, name='crear_usuario'),
   # path('editar_usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
   # path('restablecer_password/<int:id>/', views.restablecer_password, name='restablecer_password'),
   # path('eliminar_usuario/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
   # path('listado_usuarios/', views.listado_usuarios, name='listado_usuarios'),
]
