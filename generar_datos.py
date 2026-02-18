import os
import django
import random
from datetime import datetime, timedelta
from decimal import Decimal

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehiculos.settings')
django.setup()

from vehiculos.models import Vehiculo

def generar_placa():
    """Generar placa aleatoria en formato colombiano"""
    letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    numeros = ''.join(random.choices('0123456789', k=3))
    return f"{letras}{numeros}"

def generar_codigo():
    """Generar código aleatorio"""
    return f"V-{random.randint(1000, 9999)}"

def generar_cliente():
    """Generar nombre de cliente aleatorio"""
    nombres = ['Juan', 'María', 'Carlos', 'Ana', 'Luis', 'Sofía', 'Pedro', 'Laura', 'Miguel', 'Carmen']
    apellidos = ['García', 'Rodríguez', 'Martínez', 'López', 'González', 'Pérez', 'Sánchez', 'Ramírez', 'Torres', 'Díaz']
    return f"{random.choice(nombres)} {random.choice(apellidos)}"

def generar_observacion():
    """Generar observación aleatoria"""
    observaciones = [
        'Entrega realizada exitosamente',
        'Cliente solicitó entrega urgente',
        'Vehículo en buen estado',
        'Retraso por tráfico',
        'Cliente muy satisfecho',
        'Entrega en punto alternativo',
        'Sin novedades durante el viaje',
        'Cliente solicitó factura electrónica',
        'Vehículo requiere mantenimiento',
        'Entrega confirmada por teléfono'
    ]
    return random.choice(observaciones)

def generar_datos_aleatorios():
    """Generar 50 registros aleatorios de vehículos"""
    
    # Limpiar datos existentes
    Vehiculo.objects.all().delete()
    print("Datos existentes eliminados.")
    
    tipos_vehiculo = ['Turbo', 'Sencillo', 'Eléctrico']
    
    # Generar fechas base para el último mes
    fecha_base = datetime.now()
    fechas_inicio = []
    
    # Generar fechas distribuidas en el último mes
    for i in range(50):
        dias_atras = random.randint(0, 30)
        horas = random.randint(6, 18)  # Horas laborales
        minutos = random.randint(0, 59)
        fecha = fecha_base - timedelta(days=dias_atras, hours=fecha_base.hour-horas, minutes=fecha_base.minute-minutos)
        fechas_inicio.append(fecha)
    
    # Ordenar fechas de más reciente a más antigua
    fechas_inicio.sort(reverse=True)
    
    vehiculos_creados = []
    
    for i in range(50):
        fecha_inicio = fechas_inicio[i]
        # Fecha fin es entre 2 y 8 horas después
        duracion_horas = random.randint(2, 8)
        fecha_fin = fecha_inicio + timedelta(hours=duracion_horas)
        
        vehiculo = Vehiculo.objects.create(
            codigo=generar_codigo(),
            placa=generar_placa(),
            tipo_vehiculo=random.choice(tipos_vehiculo),
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin,
            numero_entregas=random.randint(1, 15),
            facturacion=Decimal(str(round(random.uniform(50000, 500000), 2))),
            observacion=generar_observacion(),
            cliente=generar_cliente(),
            validado=random.choice([True, False])
        )
        vehiculos_creados.append(vehiculo)
    
    print(f"Se han creado {len(vehiculos_creados)} registros de vehículos exitosamente.")
    
    # Mostrar estadísticas
    total_entregas = sum(v.numero_entregas for v in vehiculos_creados)
    total_facturacion = sum(v.facturacion for v in vehiculos_creados)
    validados = sum(1 for v in vehiculos_creados if v.validado)
    
    print(f"\nEstadísticas generadas:")
    print(f"- Total entregas: {total_entregas}")
    print(f"- Total facturación: ${total_facturacion:,.2f}")
    print(f"- Vehículos validados: {validados}/50 ({validados*2}%)")
    print(f"- Tipos de vehículo:")
    
    for tipo in tipos_vehiculo:
        count = Vehiculo.objects.filter(tipo_vehiculo=tipo).count()
        print(f"  * {tipo}: {count}")

if __name__ == '__main__':
    generar_datos_aleatorios()
