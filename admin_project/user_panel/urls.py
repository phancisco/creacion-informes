from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='user_panel/login.html'
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', views.menu, name='menu'),
    path('crear/', views.crear_informe, name='crear_informe'),
    path('historial/', views.historial, name='historial'),
    path('ver/<int:informe_id>/', views.ver_informe, name='ver_informe'),
    path('editar/<int:informe_id>/', views.solicitar_edicion, name='solicitar_edicion'),
    path('eliminar/<int:informe_id>/', views.solicitar_eliminacion, name='solicitar_eliminacion'),
    path('ver/pdf/<int:informe_id>/', views.ver_informe_pdf, name='ver_informe_pdf'),
]
