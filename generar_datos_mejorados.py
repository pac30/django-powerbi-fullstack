#!/usr/bin/env python
"""
Script mejorado para generar datos de prueba con campos full stack
"""
import os
import sys
import django
import random
from datetime import datetime, timedelta
from django.utils import timezone

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehiculos.settings')
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
django.setup()

from vehiculos.models import Vehiculo
from django.contrib.auth.models import User

def generar_datos_mejorados():
    """Generar 50 vehículos con datos mejorados y realistas"""
    
    # Datos para generación
    placas_base = ['ABC', 'XYZ', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STU', 'VWX', 'YZA']
    clientes = [
        'Transportes Rápidos S.A.', 'Logística Express Ltda.', 'Mensajería Veloz C.A.',
        'Distribuciones Central S.A.S.', 'Carga Segura Ltda.', 'Envíos Express C.A.',
        'Transporte Nacional S.A.', 'Logística Global Ltda.', 'Mensajería Internacional C.A.',
        'Distribuciones Rápidas S.A.S.'
    ]
    observaciones = [
        'Vehículo en excelente estado', 'Requiere mantenimiento preventivo',
        'Nuevo en la flota', 'Recientemente reparado', 'Alta prioridad',
        'Ruta regular', 'Servicio nocturno', 'Transporte especializado',
        'Vehículo de lujo', 'Equipado con GPS'
    ]
    
    # Obtener usuario admin para asignar
    try:
        admin_user = User.objects.get(username='admin')
    except User.DoesNotExist:
        print("Usuario 'admin' no encontrado. Creando usuario...")
        admin_user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    
    # Limpiar datos existentes
    Vehiculo.objects.all().delete()
    print("Datos existentes eliminados")
    
    vehiculos_creados = []
    
    for i in range(1, 51):
        # Generar placa única
        placa = f"{random.choice(placas_base)}{random.randint(100, 999)}"
        
        # Asegurar que la placa sea única
        while Vehiculo.objects.filter(placa=placa).exists():
            placa = f"{random.choice(placas_base)}{random.randint(100, 999)}"
        
        # Generar fechas realistas (últimos 30 días)
        dias_aleatorios = random.randint(0, 30)
        fecha_inicio = timezone.now() - timedelta(days=dias_aleatorios)
        duracion_horas = random.randint(4, 24)
        fecha_fin = fecha_inicio + timedelta(hours=duracion_horas)
        
        # Generar código
        codigo = f"V{i:03d}-{random.randint(1000, 9999)}"
        
        # Tipo de vehículo
        tipo_vehiculo = random.choice(['Turbo', 'Sencillo', 'Eléctrico'])
        
        # Número de entregas y facturación según tipo
        if tipo_vehiculo == 'Turbo':
            numero_entregas = random.randint(15, 50)
            facturacion = round(random.uniform(50000, 200000), 2)
            rendimiento = round(random.uniform(2.0, 5.0), 2)
        elif tipo_vehiculo == 'Sencillo':
            numero_entregas = random.randint(10, 30)
            facturacion = round(random.uniform(30000, 100000), 2)
            rendimiento = round(random.uniform(1.5, 3.5), 2)
        else:  # Eléctrico
            numero_entregas = random.randint(8, 25)
            facturacion = round(random.uniform(25000, 80000), 2)
            rendimiento = round(random.uniform(1.0, 3.0), 2)
        
        # Prioridad y estado
        prioridad = random.choices([1, 2, 3], weights=[40, 40, 20])[0]
        estado = random.choices(['activo', 'mantenimiento', 'inactivo'], weights=[70, 20, 10])[0]
        
        # Validación (70% validados)
        validado = random.random() < 0.7
        
        # Crear vehículo
        vehiculo = Vehiculo.objects.create(
            codigo=codigo,
            placa=placa,
            tipo_vehiculo=tipo_vehiculo,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            numero_entregas=numero_entregas,
            facturacion=facturacion,
            observacion=random.choice(observaciones),
            cliente=random.choice(clientes),
            validado=validado,
            usuario_creacion=admin_user,
            prioridad=prioridad,
            estado=estado,
            rendimiento=rendimiento
        )
        
        vehiculos_creados.append(vehiculo)
        print(f"Creado vehículo {i}: {placa} - {tipo_vehiculo}")
    
    # Estadísticas generadas
    total = Vehiculo.objects.count()
    validados = Vehiculo.objects.filter(validado=True).count()
    turbo_count = Vehiculo.objects.filter(tipo_vehiculo='Turbo').count()
    sencillo_count = Vehiculo.objects.filter(tipo_vehiculo='Sencillo').count()
    electrico_count = Vehiculo.objects.filter(tipo_vehiculo='Eléctrico').count()
    
    total_entregas = Vehiculo.objects.aggregate(
        total=models.Sum('numero_entregas')
    )['total'] or 0
    
    total_facturacion = Vehiculo.objects.aggregate(
        total=models.Sum('facturacion')
    )['total'] or 0
    
    print("\n" + "="*50)
    print("📊 ESTADÍSTICAS DE DATOS GENERADOS")
    print("="*50)
    print(f"🚗 Total vehículos: {total}")
    print(f"✅ Vehículos validados: {validados} ({validados/total*100:.1f}%)")
    print(f"📈 Total entregas: {total_entregas}")
    print(f"💰 Total facturación: ${total_facturacion:,.2f}")
    print(f"📋 Distribución por tipo:")
    print(f"   • Turbo: {turbo_count} ({turbo_count/total*100:.1f}%)")
    print(f"   • Sencillo: {sencillo_count} ({sencillo_count/total*100:.1f}%)")
    print(f"   • Eléctrico: {electrico_count} ({electrico_count/total*100:.1f}%)")
    print(f"🔥 Prioridad Alta: {Vehiculo.objects.filter(prioridad=3).count()}")
    print(f"⚙️ En Mantenimiento: {Vehiculo.objects.filter(estado='mantenimiento').count()}")
    print("="*50)
    print("✅ Datos generados exitosamente!")
    
    return vehiculos_creados

if __name__ == "__main__":
    try:
        from django.db import models
        vehiculos = generar_datos_mejorados()
        print(f"\n🎉 Se generaron {len(vehiculos)} vehículos con éxito!")
    except Exception as e:
        print(f"❌ Error al generar datos: {e}")
        sys.exit(1)
