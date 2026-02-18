from django.db import models
from django.core.validators import MaxLengthValidator
from django.utils import timezone


class Vehiculo(models.Model):
    TIPO_VEHICULO_CHOICES = [
        ('Turbo', 'Turbo'),
        ('Sencillo', 'Sencillo'),
        ('Eléctrico', 'Eléctrico'),
    ]
    
    codigo = models.CharField(max_length=50)
    placa = models.CharField(max_length=20)
    tipo_vehiculo = models.CharField(max_length=20, choices=TIPO_VEHICULO_CHOICES)
    fecha_inicio = models.DateTimeField()
    fecha_fin = models.DateTimeField()
    numero_entregas = models.IntegerField()
    facturacion = models.DecimalField(max_digits=10, decimal_places=2)
    observacion = models.TextField(blank=True, null=True)
    cliente = models.CharField(max_length=100, validators=[MaxLengthValidator(100)])
    validado = models.BooleanField(default=False)
    
    # Campos adicionales para full stack
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='vehiculos_creados'
    )
    usuario_modificacion = models.ForeignKey(
        'auth.User', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='vehiculos_modificados'
    )
    prioridad = models.IntegerField(
        default=1,
        choices=[
            (1, 'Baja'),
            (2, 'Media'),
            (3, 'Alta'),
        ],
        help_text='Prioridad del vehículo para procesamiento'
    )
    estado = models.CharField(
        max_length=20,
        choices=[
            ('activo', 'Activo'),
            ('mantenimiento', 'En Mantenimiento'),
            ('inactivo', 'Inactivo'),
        ],
        default='activo',
        help_text='Estado actual del vehículo'
    )
    rendimiento = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0.00,
        help_text='Índice de rendimiento (entregas/hora)'
    )
    
    class Meta:
        ordering = ['-fecha_inicio']
        verbose_name = 'Vehículo'
        verbose_name_plural = 'Vehículos'
        indexes = [
            models.Index(fields=['placa']),
            models.Index(fields=['fecha_inicio']),
            models.Index(fields=['validado']),
            models.Index(fields=['tipo_vehiculo']),
        ]
    
    def __str__(self):
        return f"{self.placa} - {self.codigo}"
    
    @property
    def duracion_horas(self):
        """Calcular duración en horas"""
        if self.fecha_fin and self.fecha_inicio:
            delta = self.fecha_fin - self.fecha_inicio
            return round(delta.total_seconds() / 3600, 2)
        return 0
    
    @property
    def eficiencia(self):
        """Calcular eficiencia (entregas/hora)"""
        duracion = self.duracion_horas
        if duracion > 0:
            return round(self.numero_entregas / duracion, 2)
        return 0
    
    @property
    def facturacion_por_entrega(self):
        """Calcular facturación por entrega"""
        if self.numero_entregas > 0:
            return round(float(self.facturacion) / self.numero_entregas, 2)
        return 0
