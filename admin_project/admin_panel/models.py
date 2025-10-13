from django.db import models
from django.contrib.auth.models import User

class Taller(models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=200)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

class PerfilUsuario(models.Model):
    ROLES = [
        ('inspector', 'Inspector de Calidad'),
        ('jefe', 'Jefe de Taller'),
        ('admin', 'Administrador'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    run = models.CharField(max_length=12, unique=True)
    telefono = models.CharField(max_length=15, blank=True)
    rol = models.CharField(max_length=20, choices=ROLES, default='inspector')
    taller = models.ForeignKey(Taller, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.get_rol_display()}"

class ParametroObligatorio(models.Model):
    numero = models.IntegerField(unique=True)
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['numero']
    
    def __str__(self):
        return f"{self.numero}. {self.descripcion[:50]}..."

class ParametroOpcional(models.Model):
    descripcion = models.TextField()
    activo = models.BooleanField(default=True)
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.descripcion[:50]}..."

class Informe(models.Model):
    ESTADOS = [
        ('borrador', 'Borrador'),
        ('completado', 'Completado'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    ]
    
    numero_os = models.CharField(max_length=50)
    marca = models.CharField(max_length=100)
    componente = models.CharField(max_length=100)
    cliente = models.CharField(max_length=200)
    aplicacion = models.CharField(max_length=100)
    inspector = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_liberacion = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='borrador')
    
    def __str__(self):
        return f"Informe {self.numero_os} - {self.cliente}"

class SolicitudCambio(models.Model):
    TIPOS = [
        ('parametro', 'Modificación Parámetro'),
        ('eliminacion', 'Eliminación Informe'),
        ('usuario', 'Modificación Usuario'),
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    
    usuario_solicitante = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    descripcion = models.TextField()
    justificacion = models.TextField()
    fecha_solicitud = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    aprobado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitudes_aprobadas')
    fecha_respuesta = models.DateTimeField(null=True, blank=True)
    comentarios_admin = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.get_tipo_display()} - {self.usuario_solicitante.username}"
