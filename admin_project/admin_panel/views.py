from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *


PARAMETROS_OBLIGATORIOS = [
    "Verificar que todas las zonas de acople se encuentren libres de pintura",
    "Verificar el estado de todos los hilos",
    "Verificar la correcta instalación y conexión de los sensores",
    "Verificar la correcta instalación del arnés",
    "Verificar la aplicación de anti-sabotaje en toda la periferia externa",
    "Verificar instalación de tapones plásticos en agujeros con hilos",
    "Verificar que todos los tapones estén pintados de color rojo",
    "Verificar que el estado de la pintura del componente sea óptimo",
    "Verificar la instalación de placa y OS",
    "Verificar la instalación de todos los accesorios (Si aplica)",
    "Verificar la instalación de todas las tapas de traslado",
    "Verificar la aplicación de grasa antioxidante en zonas no pintadas",
    "Verificar que todos los hilos de izaje se encuentren en condiciones óptimas de uso",
    "Verificar que la base de traslado se encuentre en buenas condiciones",
    "Revisar instalación, posición y orientación de mirilla de nivel de aceite",
    "Verificar que proceso de pre-embalaje y componente embalado sea óptimo"
]

@login_required
def dashboard(request):
    total_informes = Informe.objects.count()
    usuarios_activos = User.objects.filter(is_active=True).count()
    solicitudes_pendientes = SolicitudCambio.objects.filter(estado='pendiente').count()
    
    context = {
        'total_informes': total_informes,
        'usuarios_activos': usuarios_activos,
        'solicitudes_pendientes': solicitudes_pendientes,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
def usuarios_lista(request):
    usuarios = PerfilUsuario.objects.select_related('usuario', 'taller').all()
    talleres = Taller.objects.filter(activo=True)
    
    context = {
        'usuarios': usuarios,
        'talleres': talleres,
    }
    return render(request, 'admin_panel/usuarios_lista.html', context)

@login_required
def parametros_configuracion(request):
    parametros_obligatorios_lista = []
    for i, descripcion in enumerate(PARAMETROS_OBLIGATORIOS, 1):
        parametros_obligatorios_lista.append({
            'numero': i,
            'descripcion': descripcion,
            'activo': True
        })
    
    parametros_opcionales = ParametroOpcional.objects.filter(activo=True).order_by('fecha_creacion')
    
    context = {
        'parametros_obligatorios': parametros_obligatorios_lista,
        'parametros_opcionales': parametros_opcionales,
    }
    return render(request, 'admin_panel/parametros_configuracion.html', context)

@login_required
def solicitudes_cambio(request):
    solicitudes = SolicitudCambio.objects.filter(estado='pendiente').order_by('-fecha_solicitud')
    
    context = {
        'solicitudes': solicitudes,
    }
    return render(request, 'admin_panel/solicitudes_cambio.html', context)

@login_required
def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCambio, id=solicitud_id)
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        comentarios = request.POST.get('comentarios', '')
        
        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
            messages.success(request, 'Solicitud aprobada exitosamente')
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
            messages.success(request, 'Solicitud rechazada')
        
        solicitud.aprobado_por = request.user
        solicitud.fecha_respuesta = timezone.now()
        solicitud.comentarios_admin = comentarios
        solicitud.save()
    
    return redirect('solicitudes_cambio')

@login_required
def monitoreo_informes(request):
    informes_recientes = Informe.objects.select_related('inspector').order_by('-fecha_creacion')[:20]
    
    context = {
        'informes_recientes': informes_recientes,
    }
    return render(request, 'admin_panel/monitoreo_informes.html', context)

@login_required
def auditoria_completa(request):
    # Aquí puedes agregar lógica más compleja para auditoría
    cambios_recientes = SolicitudCambio.objects.select_related('usuario_solicitante', 'aprobado_por').order_by('-fecha_solicitud')[:50]
    
    context = {
        'cambios_recientes': cambios_recientes,
    }
    return render(request, 'admin_panel/auditoria_completa.html', context)