from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('usuarios/crear/', views.crear_usuario, name='crear_usuario'),
    path('usuarios/editar/<int:perfil_id>/', views.editar_usuario, name='editar_usuario'),
    path('usuarios/eliminar/<int:perfil_id>/', views.eliminar_usuario, name='eliminar_usuario'),
    path('parametros/', views.parametros_configuracion, name='parametros_configuracion'),
    path('parametros/crear/', views.crear_parametro_opcional, name='crear_parametro_opcional'),
    path('parametros/editar/<int:parametro_id>/', views.editar_parametro_opcional, name='editar_parametro_opcional'),
    path('parametros/eliminar/<int:parametro_id>/', views.eliminar_parametro_opcional, name='eliminar_parametro_opcional'),
    path('solicitudes/', views.solicitudes_cambio, name='solicitudes_cambio'),
    path('solicitudes/aprobar/<int:solicitud_id>/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('monitoreo/', views.monitoreo_informes, name='monitoreo_informes'),
    path('auditoria/', views.auditoria_completa, name='auditoria_completa'),
    path('pdf/', views.administracion_pdf, name='administracion_pdf'),
]