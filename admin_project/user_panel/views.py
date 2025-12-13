from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from admin_panel.models import (
    Informe,
    ParametroObligatorio,
    ParametroOpcional,
    RespuestaParametro,
    SolicitudCambio,
    Componente,
)

# =========================
# MENÚ PRINCIPAL
# =========================
@login_required
def menu(request):
    return render(request, 'user_panel/menu.html')


# =========================
# CREAR INFORME
# =========================
@login_required
def crear_informe(request):
    if request.method == 'POST':

        informe = Informe.objects.create(
            numero_os=request.POST.get('numero_os'),
            marca=request.POST.get('marca'),
            componente_id=request.POST.get('componente'),
            aplicacion=request.POST.get('aplicacion'),
            cliente=request.POST.get('cliente'),
            autor=request.user,
            inspector=request.user,
        )

        obligatorios = ParametroObligatorio.objects.filter(activo=True)

        for p in obligatorios:
            if f'obl_{p.id}' not in request.POST:
                messages.error(
                    request,
                    'Debes marcar todos los parámetros obligatorios'
                )
                informe.delete()
                return redirect('crear_informe')

        # Guardar respuestas obligatorias
        for p in obligatorios:
            RespuestaParametro.objects.create(
                informe=informe,
                parametro_obligatorio=p,
                aprobado=True
            )

        # Guardar respuestas opcionales (solo si están marcados)
        opcionales = ParametroOpcional.objects.filter(activo=True)
        for p in opcionales:
            if f'opc_{p.id}' in request.POST:
                RespuestaParametro.objects.create(
                    informe=informe,
                    parametro_opcional=p,
                    aprobado=True
                )

        messages.success(request, 'Informe creado correctamente')
        return redirect('historial')

    context = {
        'obligatorios': ParametroObligatorio.objects.filter(activo=True),
        'opcionales': ParametroOpcional.objects.filter(activo=True),
        'componentes': Componente.objects.filter(activo=True),
    }

    return render(request, 'user_panel/crear_informe.html', context)


# =========================
# HISTORIAL
# =========================
@login_required
def historial(request):
    # Exclude informes that have a pending deletion request
    pending_ids = SolicitudCambio.objects.filter(
        tipo='eliminacion', estado='pendiente'
    ).values_list('informe_id', flat=True)

    informes = Informe.objects.filter(
        inspector=request.user
    ).exclude(id__in=pending_ids).order_by('-fecha_creacion')

    return render(request, 'user_panel/historial.html', {
        'informes': informes
    })

# =========================
# VER INFORME
# =========================
@login_required
def ver_informe(request, informe_id):
    informe = get_object_or_404(
        Informe,
        id=informe_id,
        inspector=request.user
    )
    # If there's a pending deletion request for this informe, block viewing
    if SolicitudCambio.objects.filter(informe=informe, tipo='eliminacion', estado='pendiente').exists():
        messages.error(request, 'Este informe está en revisión y no se puede ver actualmente.')
        return redirect('historial')

    return render(request, 'user_panel/ver_informe.html', {
        'informe': informe
    })


# =========================
# SOLICITAR EDICIÓN
# =========================
@login_required
def solicitar_edicion(request, informe_id):
    informe = get_object_or_404(
        Informe,
        id=informe_id,
        inspector=request.user
    )

    if request.method == 'POST':
        # Build proposed changes dict
        cambios = {}
        if request.POST.get('marca') != informe.marca:
            cambios['marca'] = request.POST.get('marca')
        if request.POST.get('cliente') != informe.cliente:
            cambios['cliente'] = request.POST.get('cliente')
        if request.POST.get('aplicacion') != informe.aplicacion:
            cambios['aplicacion'] = request.POST.get('aplicacion')
        if request.POST.get('componente') and str(informe.componente_id) != request.POST.get('componente'):
            cambios['componente_id'] = int(request.POST.get('componente'))

        # Capture proposed parameter approval changes
        respuestas_propuestas = {'obligatorios': {}, 'opcionales': {}}
        for p in ParametroObligatorio.objects.filter(activo=True):
            field = f'obl_{p.id}'
            respuestas_propuestas['obligatorios'][str(p.id)] = (field in request.POST)

        for p in ParametroOpcional.objects.filter(activo=True):
            field = f'opc_{p.id}'
            respuestas_propuestas['opcionales'][str(p.id)] = (field in request.POST)

        SolicitudCambio.objects.create(
            usuario_solicitante=request.user,
            tipo='parametro',
            descripcion=f'Solicitud de edición del informe OS {informe.numero_os}',
            justificacion=request.POST['justificacion'],
            informe=informe,
            propuesta_campos={
                **(cambios if cambios else {}),
                'respuestas': respuestas_propuestas
            },
        )

        messages.success(request, 'Solicitud enviada a administración')
        return redirect('historial')

    # Prepare current responses to pre-fill the form
    respuestas = informe.respuestas.all()
    respuestas_obl_ids = [r.parametro_obligatorio.id for r in respuestas if r.parametro_obligatorio and r.aprobado]
    respuestas_opc_ids = [r.parametro_opcional.id for r in respuestas if r.parametro_opcional and r.aprobado]

    return render(request, 'user_panel/solicitar_edicion.html', {
        'informe': informe,
        'componentes': Componente.objects.filter(activo=True),
        'obligatorios': ParametroObligatorio.objects.filter(activo=True),
        'opcionales': ParametroOpcional.objects.filter(activo=True),
        'respuestas_obl_ids': respuestas_obl_ids,
        'respuestas_opc_ids': respuestas_opc_ids,
    })


# =========================
# SOLICITAR ELIMINACIÓN
# =========================
@login_required
def solicitar_eliminacion(request, informe_id):
    informe = get_object_or_404(
        Informe,
        id=informe_id,
        inspector=request.user
    )

    # If there's a pending deletion request already, redirect to historial
    if SolicitudCambio.objects.filter(informe=informe, tipo='eliminacion', estado='pendiente').exists():
        messages.info(request, 'Ya existe una solicitud de eliminación en revisión para este informe.')
        return redirect('historial')

    if request.method == 'POST':
        # Prevent duplicate pending deletion requests
        if SolicitudCambio.objects.filter(informe=informe, tipo='eliminacion', estado='pendiente').exists():
            messages.info(request, 'Ya hay una solicitud de eliminación en revisión para este informe.')
            return redirect('historial')
        SolicitudCambio.objects.create(
            usuario_solicitante=request.user,
            tipo='eliminacion',
            descripcion=f'Solicitud de eliminación del informe OS {informe.numero_os}',
            justificacion=request.POST['justificacion']
            ,
            informe=informe,
        )

        messages.success(request, 'Solicitud enviada a administración')
        return redirect('historial')

    return render(request, 'user_panel/solicitar_eliminacion.html', {
        'informe': informe
    })



@login_required
def ver_informe_pdf(request, informe_id):
    informe = get_object_or_404(
        Informe,
        id=informe_id,
        inspector=request.user
    )
    # Try to import an optional PDF library and render template; fail gracefully
    try:
        from django.template.loader import render_to_string
        from xhtml2pdf import pisa
        import io

        html = render_to_string('user_panel/ver_informe_pdf.html', {'informe': informe})
        result = io.BytesIO()
        pdf = pisa.CreatePDF(html, dest=result)
        if pdf.err:
            return HttpResponse('Error generando PDF', status=500)
        response = HttpResponse(result.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="informe_{informe.numero_os}.pdf"'
        return response
    except Exception:
        messages.error(request, 'No se pudo generar el PDF. Instala xhtml2pdf.')
        return redirect('ver_informe', informe_id=informe.id)
