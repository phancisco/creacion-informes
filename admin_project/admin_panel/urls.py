from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('usuarios/', views.usuarios_lista, name='usuarios_lista'),
    path('parametros/', views.parametros_configuracion, name='parametros_configuracion'),
    path('solicitudes/', views.solicitudes_cambio, name='solicitudes_cambio'),
    path('solicitudes/aprobar/<int:solicitud_id>/', views.aprobar_solicitud, name='aprobar_solicitud'),
    path('monitoreo/', views.monitoreo_informes, name='monitoreo_informes'),
    path('auditoria/', views.auditoria_completa, name='auditoria_completa'),
]