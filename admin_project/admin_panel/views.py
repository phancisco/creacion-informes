from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *

# Lista de los 16 parámetros obligatorios hardcodeados
parametros_obligatorios = ParametroObligatorio.objects.filter(activo=True)

def dashboard(request):
    # Estadísticas básicas - solo usuarios con perfil (creados desde la app)
    total_informes = Informe.objects.count()
    usuarios_activos = PerfilUsuario.objects.filter(usuario__is_active=True).count()
    solicitudes_pendientes = SolicitudCambio.objects.filter(estado='pendiente').count()
    
    context = {
        'total_informes': total_informes,
        'usuarios_activos': usuarios_activos,
        'solicitudes_pendientes': solicitudes_pendientes,
    }
    return render(request, 'admin_panel/dashboard.html', context)


def usuarios_lista(request):
    usuarios = PerfilUsuario.objects.select_related('usuario').all()
    
    context = {
        'usuarios': usuarios,
    }
    return render(request, 'admin_panel/usuarios_lista.html', context)


def parametros_configuracion(request):
    # Crear lista de parámetros obligatorios con números
    parametros_obligatorios_lista = []
    for i, descripcion in enumerate(parametros_obligatorios, 1):
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

def solicitudes_cambio(request):
    # Only admin users should access this
    if not (request.user.is_superuser or getattr(getattr(request.user, 'perfilusuario', None), 'rol', None) == 'admin'):
        messages.error(request, 'Acceso denegado')
        return redirect('dashboard')

    solicitudes = SolicitudCambio.objects.filter(estado='pendiente').order_by('-fecha_solicitud')
    
    context = {
        'solicitudes': solicitudes,
    }
    return render(request, 'admin_panel/solicitudes_cambio.html', context)

def aprobar_solicitud(request, solicitud_id):
    solicitud = get_object_or_404(SolicitudCambio, id=solicitud_id)
    if not (request.user.is_superuser or getattr(getattr(request.user, 'perfilusuario', None), 'rol', None) == 'admin'):
        messages.error(request, 'Acción no permitida')
        return redirect('solicitudes_cambio')
    
    if request.method == 'POST':
        accion = request.POST.get('accion')
        comentarios = request.POST.get('comentarios', '')
        
        if accion == 'aprobar':
            solicitud.estado = 'aprobada'
            # Si la solicitud es de eliminación, eliminar el informe asociado
            if solicitud.tipo == 'eliminacion' and solicitud.informe:
                informe = solicitud.informe
                informe_num = informe.numero_os
                informe.delete()
                solicitud.informe = None
                messages.success(request, f'Informe {informe_num} eliminado y solicitud aprobada')
            # Si la solicitud es de edición, aplicar cambios propuestos
            elif solicitud.tipo == 'parametro' and solicitud.informe and solicitud.propuesta_campos:
                informe = solicitud.informe
                data = solicitud.propuesta_campos
                if 'marca' in data:
                    informe.marca = data['marca']
                if 'cliente' in data:
                    informe.cliente = data['cliente']
                if 'aplicacion' in data:
                    informe.aplicacion = data['aplicacion']
                if 'componente_id' in data:
                    from .models import Componente as Comp
                    try:
                        comp = Comp.objects.get(id=data['componente_id'])
                        informe.componente = comp
                    except Comp.DoesNotExist:
                        pass
                # Apply parameter response changes if present
                if 'respuestas' in data:
                    respuestas = data['respuestas']
                    # Obligatorios
                    for pid_str, aprobado in respuestas.get('obligatorios', {}).items():
                        try:
                            pid = int(pid_str)
                            p = ParametroObligatorio.objects.get(id=pid)
                            rp, created = RespuestaParametro.objects.get_or_create(
                                informe=informe,
                                parametro_obligatorio=p,
                                defaults={'aprobado': bool(aprobado)}
                            )
                            if not created:
                                rp.aprobado = bool(aprobado)
                                rp.save()
                        except ParametroObligatorio.DoesNotExist:
                            continue

                    # Opcionales
                    for pid_str, aprobado in respuestas.get('opcionales', {}).items():
                        try:
                            pid = int(pid_str)
                            p = ParametroOpcional.objects.get(id=pid)
                            rp, created = RespuestaParametro.objects.get_or_create(
                                informe=informe,
                                parametro_opcional=p,
                                defaults={'aprobado': bool(aprobado)}
                            )
                            if not created:
                                rp.aprobado = bool(aprobado)
                                rp.save()
                        except ParametroOpcional.DoesNotExist:
                            continue

                informe.save()
                messages.success(request, 'Solicitud aprobada y cambios aplicados al informe')
            else:
                messages.success(request, 'Solicitud aprobada exitosamente')
        elif accion == 'rechazar':
            solicitud.estado = 'rechazada'
            messages.success(request, 'Solicitud rechazada')
        
        solicitud.aprobado_por = request.user
        solicitud.fecha_respuesta = timezone.now()
        solicitud.comentarios_admin = comentarios
        solicitud.save()
    
    return redirect('solicitudes_cambio')

def monitoreo_informes(request):
    informes_recientes = Informe.objects.select_related('inspector').order_by('-fecha_creacion')[:20]
    
    context = {
        'informes_recientes': informes_recientes,
    }
    return render(request, 'admin_panel/monitoreo_informes.html', context)

def auditoria_completa(request):
    # Aquí puedes agregar lógica más compleja para auditoría
    cambios_recientes = SolicitudCambio.objects.select_related('usuario_solicitante', 'aprobado_por').order_by('-fecha_solicitud')[:50]
    
    context = {
        'cambios_recientes': cambios_recientes,
    }
    return render(request, 'admin_panel/auditoria_completa.html', context)

# Nuevas vistas para crear usuarios
def crear_usuario(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        run = request.POST.get('run')
        rol = request.POST.get('rol')
        taller = request.POST.get('taller')
        telefono = request.POST.get('telefono', '')
        
        # Crear usuario
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )
        
        # Crear perfil
        PerfilUsuario.objects.create(
            usuario=user,
            run=run,
            rol=rol,
            taller=taller,
            telefono=telefono
        )
        
        messages.success(request, f'Usuario {username} creado exitosamente')
        return redirect('usuarios_lista')
    
    return render(request, 'admin_panel/crear_usuario.html')

# Nueva vista para crear parámetro opcional
def crear_parametro_opcional(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        activo = request.POST.get('activo') == 'on'
        
        # Usar superusuario si no hay usuario logueado
        usuario = request.user if request.user.is_authenticated else User.objects.filter(is_superuser=True).first()
        
        ParametroOpcional.objects.create(
            descripcion=descripcion,
            activo=activo,
            creado_por=usuario
        )
        
        messages.success(request, 'Parámetro opcional creado exitosamente')
        return redirect('parametros_configuracion')
    
    return render(request, 'admin_panel/crear_parametro_opcional.html')


def editar_usuario(request, perfil_id):
    perfil = get_object_or_404(PerfilUsuario, id=perfil_id)
    
    if request.method == 'POST':
        perfil.usuario.username = request.POST.get('username')
        perfil.usuario.email = request.POST.get('email')
        perfil.usuario.first_name = request.POST.get('first_name')
        perfil.usuario.last_name = request.POST.get('last_name')
        
        password = request.POST.get('password')
        if password:
            perfil.usuario.set_password(password)
        
        perfil.usuario.save()
        
        perfil.run = request.POST.get('run')
        perfil.rol = request.POST.get('rol')
        perfil.telefono = request.POST.get('telefono', '')
        perfil.taller = request.POST.get('taller')
        perfil.save()
        
        messages.success(request, f'Usuario {perfil.usuario.username} actualizado exitosamente')
        return redirect('usuarios_lista')
    
    context = {'perfil': perfil}
    return render(request, 'admin_panel/editar_usuario.html', context)

# Eliminar usuario
def eliminar_usuario(request, perfil_id):
    if request.method == 'POST':
        perfil = get_object_or_404(PerfilUsuario, id=perfil_id)
        username = perfil.usuario.username
        perfil.usuario.delete()
        messages.success(request, f'Usuario {username} eliminado exitosamente')
    return redirect('usuarios_lista')

# Editar parámetro opcional
def editar_parametro_opcional(request, parametro_id):
    parametro = get_object_or_404(ParametroOpcional, id=parametro_id)
    
    if request.method == 'POST':
        parametro.descripcion = request.POST.get('descripcion')
        parametro.activo = request.POST.get('activo') == 'on'
        parametro.save()
        
        messages.success(request, 'Parámetro actualizado exitosamente')
        return redirect('parametros_configuracion')
    
    context = {'parametro': parametro}
    return render(request, 'admin_panel/editar_parametro_opcional.html', context)

# Eliminar parámetro opcional
def eliminar_parametro_opcional(request, parametro_id):
    if request.method == 'POST':
        parametro = get_object_or_404(ParametroOpcional, id=parametro_id)
        parametro.delete()
        messages.success(request, 'Parámetro eliminado exitosamente')
    return redirect('parametros_configuracion')

def administracion_pdf(request):
    context = {}
    return render(request, 'admin_panel/administracion_pdf.html', context)