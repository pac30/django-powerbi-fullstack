import os
import django
import pandas as pd
from datetime import datetime

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_vehiculos.settings')
django.setup()

from vehiculos.models import Vehiculo

def exportar_datos_ejemplo():
    """Exportar todos los datos a Excel para Power BI"""
    
    # Obtener todos los vehículos
    vehiculos = Vehiculo.objects.all().order_by('-fecha_inicio')
    
    # Crear datos para Excel
    data = []
    for vehiculo in vehiculos:
        data.append({
            'Código': vehiculo.codigo,
            'Placa': vehiculo.placa,
            'Tipo Vehículo': vehiculo.tipo_vehiculo,
            'Fecha Inicio': vehiculo.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
            'Fecha Fin': vehiculo.fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
            'Número Entregas': vehiculo.numero_entregas,
            'Facturación': float(vehiculo.facturacion),
            'Observación': vehiculo.observacion or '',
            'Cliente': vehiculo.cliente,
            'Validado': 'Sí' if vehiculo.validado else 'No',
            'Día': vehiculo.fecha_inicio.date(),
            'Mes': vehiculo.fecha_inicio.strftime('%Y-%m'),
            'Año': vehiculo.fecha_inicio.year
        })
    
    # Crear DataFrame
    df = pd.DataFrame(data)
    
    # Exportar a Excel
    filename = f'vehiculos_powerbi_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
    filepath = os.path.join(os.getcwd(), filename)
    
    df.to_excel(filepath, index=False, engine='openpyxl')
    
    print(f"✅ Archivo exportado: {filename}")
    print(f"📊 Total registros: {len(data)}")
    
    # Estadísticas para Power BI
    total_entregas = df['Número Entregas'].sum()
    total_facturacion = df['Facturación'].sum()
    validados = len(df[df['Validado'] == 'Sí'])
    
    print(f"\n📈 Estadísticas para Power BI:")
    print(f"   • Total entregas: {total_entregas:,}")
    print(f"   • Total facturación: ${total_facturacion:,.2f}")
    print(f"   • Vehículos validados: {validados}/{len(df)} ({validados/len(df)*100:.1f}%)")
    
    # Distribución por tipo
    print(f"\n🚗 Distribución por tipo:")
    for tipo in df['Tipo Vehículo'].unique():
        count = len(df[df['Tipo Vehículo'] == tipo])
        print(f"   • {tipo}: {count}")
    
    # Distribución por día
    print(f"\n📅 Distribución por día (últimos 10 días):")
    daily_counts = df.groupby('Día').size().sort_values(ascending=False).head(10)
    for day, count in daily_counts.items():
        print(f"   • {day.strftime('%d/%m/%Y')}: {count} vehículos")
    
    return filepath

if __name__ == '__main__':
    exportar_datos_ejemplo()
