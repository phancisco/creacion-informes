from django.contrib import admin
from .models import *

@admin.register(Taller)
class TallerAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ubicacion', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre', 'ubicacion']

@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'run', 'rol', 'taller']
    list_filter = ['rol', 'taller']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'run']

@admin.register(ParametroObligatorio)
class ParametroObligatorioAdmin(admin.ModelAdmin):
    list_display = ['numero', 'descripcion_corta', 'activo']
    list_filter = ['activo']
    ordering = ['numero']
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + "..." if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

@admin.register(ParametroOpcional)
class ParametroOpcionalAdmin(admin.ModelAdmin):
    list_display = ['descripcion_corta', 'activo', 'creado_por', 'fecha_creacion']
    list_filter = ['activo', 'fecha_creacion']
    
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + "..." if len(obj.descripcion) > 50 else obj.descripcion
    descripcion_corta.short_description = 'Descripción'

@admin.register(Informe)
class InformeAdmin(admin.ModelAdmin):
    list_display = ['numero_os', 'cliente', 'inspector', 'fecha_creacion']
    list_filter = ['fecha_creacion', 'inspector']
    search_fields = ['numero_os', 'cliente', 'marca', 'componente']

@admin.register(SolicitudCambio)
class SolicitudCambioAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'usuario_solicitante', 'informe', 'propuesta_campos', 'estado', 'fecha_solicitud']
    list_filter = ['tipo', 'estado', 'fecha_solicitud']
    search_fields = ['descripcion', 'usuario_solicitante__username']

@admin.register(Componente)
class ComponenteAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'activo']
    list_filter = ['activo']
    search_fields = ['nombre']
