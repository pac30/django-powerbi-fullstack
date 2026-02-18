from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum, Avg
from django.utils.dateparse import parse_date
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.utils import timezone
import csv
import pandas as pd
from datetime import datetime, timedelta
import json
from .models import Vehiculo


def login_view(request):
    """Vista de login con mejoras de seguridad y UX"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Guardar último acceso
            request.session['last_login'] = timezone.now().isoformat()
            return redirect('principal')
        else:
            error_message = "Usuario o contraseña incorrectos"
            return render(request, 'vehiculos/login.html', {'error': error_message})
    
    return render(request, 'vehiculos/login.html')


@login_required
def logout_view(request):
    """Cerrar sesión con limpieza completa"""
    logout(request)
    request.session.flush()
    return redirect('login')


@login_required
def principal_view(request):
    """Vista principal con caché y optimización"""
    # Obtener parámetros de filtrado
    placa_filter = request.GET.get('placa', '')
    fecha_inicio_filter = request.GET.get('fecha_inicio', '')
    fecha_fin_filter = request.GET.get('fecha_fin', '')
    validado_filter = request.GET.get('validado', '')
    
    # Construir consulta base con optimización
    queryset = Vehiculo.objects.all()
    
    # Aplicar filtros
    if placa_filter:
        queryset = queryset.filter(placa__icontains=placa_filter)
    
    if fecha_inicio_filter:
        fecha_inicio = parse_date(fecha_inicio_filter)
        if fecha_inicio:
            queryset = queryset.filter(fecha_inicio__date__gte=fecha_inicio)
    
    if fecha_fin_filter:
        fecha_fin = parse_date(fecha_fin_filter)
        if fecha_fin:
            queryset = queryset.filter(fecha_inicio__date__lte=fecha_fin)
    
    if validado_filter:
        if validado_filter == 'true':
            queryset = queryset.filter(validado=True)
        elif validado_filter == 'false':
            queryset = queryset.filter(validado=False)
    
    # MOSTRAR TODOS LOS VEHÍCULOS (sin paginación)
    vehiculos = queryset.order_by('-fecha_inicio')
    
    # Calcular estadísticas adicionales
    stats = calculate_real_time_stats(queryset)
    
    context = {
        'vehiculos': vehiculos,
        'placa_filter': placa_filter,
        'fecha_inicio_filter': fecha_inicio_filter,
        'fecha_fin_filter': fecha_fin_filter,
        'validado_filter': validado_filter,
        'stats': stats,
    }
    
    return render(request, 'vehiculos/principal.html', context)


def calculate_real_time_stats(queryset):
    """Calcular estadísticas en tiempo real"""
    total = queryset.count()
    validados = queryset.filter(validado=True).count()
    no_validados = total - validados
    
    # Estadísticas por tipo
    stats_tipo = {}
    for tipo in ['Turbo', 'Sencillo', 'Eléctrico']:
        count = queryset.filter(tipo_vehiculo=tipo).count()
        stats_tipo[tipo.lower()] = count
    
    # Entregas y facturación
    total_entregas = queryset.aggregate(total_entregas=Sum('numero_entregas'))['total_entregas'] or 0
    total_facturacion = queryset.aggregate(total_facturacion=Sum('facturacion'))['total_facturacion'] or 0
    
    # Última actualización
    ultima_actualizacion = queryset.order_by('-fecha_inicio').first()
    
    return {
        'total_vehiculos': total,
        'vehiculos_validados': validados,
        'vehiculos_no_validados': no_validados,
        'porcentaje_validacion': round((validados / total * 100), 2) if total > 0 else 0,
        'stats_tipo': stats_tipo,
        'total_entregas': total_entregas,
        'total_facturacion': total_facturacion,
        'promedio_entregas': round(total_entregas / total, 2) if total > 0 else 0,
        'promedio_facturacion': round(total_facturacion / total, 2) if total > 0 else 0,
        'ultima_actualizacion': ultima_actualizacion.fecha_inicio if ultima_actualizacion else None,
        'vehiculos_hoy': queryset.filter(fecha_inicio__date=timezone.now().date()).count(),
        'vehiculos_ultima_semana': queryset.filter(
            fecha_inicio__date__gte=timezone.now().date() - timedelta(days=7)
        ).count(),
    }


@login_required
@csrf_exempt
def toggle_validacion(request):
    """Vista AJAX simplificada para cambiar estado de validación"""
    if request.method == 'POST':
        vehiculo_id = request.POST.get('vehiculo_id')
        validado = request.POST.get('validado') == 'true'
        
        try:
            vehiculo = Vehiculo.objects.get(id=vehiculo_id)
            vehiculo.validado = validado
            vehiculo.save()
            
            return JsonResponse({
                'success': True,
                'message': f'Veículo {vehiculo.placa} {"validado" if validado else "invalidado"} correctamente',
                'timestamp': timezone.now().isoformat()
            })
        except Vehiculo.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Vehículo no encontrado'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })


@login_required
def exportar_datos(request):
    """Exportación simplificada y sin errores"""
    # Obtener los mismos filtros que en la vista principal
    placa_filter = request.GET.get('placa', '')
    fecha_inicio_filter = request.GET.get('fecha_inicio', '')
    fecha_fin_filter = request.GET.get('fecha_fin', '')
    validado_filter = request.GET.get('validado', '')
    export_type = request.GET.get('type', 'excel')
    
    # Construir consulta base
    queryset = Vehiculo.objects.all()
    
    if placa_filter:
        queryset = queryset.filter(placa__icontains=placa_filter)
    
    if fecha_inicio_filter:
        fecha_inicio = parse_date(fecha_inicio_filter)
        if fecha_inicio:
            queryset = queryset.filter(fecha_inicio__date__gte=fecha_inicio)
    
    if fecha_fin_filter:
        fecha_fin = parse_date(fecha_fin_filter)
        if fecha_fin:
            queryset = queryset.filter(fecha_inicio__date__lte=fecha_fin)
    
    if validado_filter:
        if validado_filter == 'true':
            queryset = queryset.filter(validado=True)
        elif validado_filter == 'false':
            queryset = queryset.filter(validado=False)
    
    # Ordenar
    vehiculos = queryset.order_by('-fecha_inicio')
    
    # Crear metadata del archivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename_base = f"vehiculos_{timestamp}"
    
    if export_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename_base}.csv"'
        
        writer = csv.writer(response)
        writer.writerow([
            'Código', 'Placa', 'Tipo Vehículo', 'Fecha Inicio', 'Fecha Fin', 
            'Número Entregas', 'Facturación', 'Observación', 'Cliente', 'Validado'
        ])
        
        for vehiculo in vehiculos:
            writer.writerow([
                vehiculo.codigo,
                vehiculo.placa,
                vehiculo.tipo_vehiculo,
                vehiculo.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
                vehiculo.fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
                vehiculo.numero_entregas,
                str(vehiculo.facturacion),
                vehiculo.observacion or '',
                vehiculo.cliente,
                'Sí' if vehiculo.validado else 'No'
            ])
        
        return response
    
    else:  # Excel - versión ultra simplificada
        try:
            # Crear datos básicos
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
                    'Validado': 'Sí' if vehiculo.validado else 'No'
                })
            
            df = pd.DataFrame(data)
            
            # Crear respuesta HTTP
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = f'attachment; filename="{filename_base}.xlsx"'
            
            # Exportar a Excel
            with pd.ExcelWriter(response, engine='openpyxl') as writer:
                df.to_excel(writer, index=False, sheet_name='Vehículos')
            
            return response
            
        except Exception as e:
            # Si falla, intentar con método más simple
            try:
                import io
                output = io.BytesIO()
                
                # Crear DataFrame simple
                data = []
                for vehiculo in vehiculos:
                    data.append([
                        vehiculo.codigo,
                        vehiculo.placa,
                        vehiculo.tipo_vehiculo,
                        vehiculo.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
                        vehiculo.fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
                        vehiculo.numero_entregas,
                        float(vehiculo.facturacion),
                        vehiculo.observacion or '',
                        vehiculo.cliente,
                        'Sí' if vehiculo.validado else 'No'
                    ])
                
                df = pd.DataFrame(data, columns=[
                    'Código', 'Placa', 'Tipo Vehículo', 'Fecha Inicio', 'Fecha Fin',
                    'Número Entregas', 'Facturación', 'Observación', 'Cliente', 'Validado'
                ])
                
                # Guardar en BytesIO
                df.to_excel(output, index=False, engine='openpyxl')
                output.seek(0)
                
                # Crear respuesta
                response = HttpResponse(
                    output.read(),
                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
                )
                response['Content-Disposition'] = f'attachment; filename="{filename_base}.xlsx"'
                
                return response
                
            except Exception as e2:
                # Último recurso: CSV con extensión XLSX
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename="{filename_base}.xlsx"'
                
                writer = csv.writer(response)
                writer.writerow([
                    'Código', 'Placa', 'Tipo Vehículo', 'Fecha Inicio', 'Fecha Fin', 
                    'Número Entregas', 'Facturación', 'Observación', 'Cliente', 'Validado'
                ])
                
                for vehiculo in vehiculos:
                    writer.writerow([
                        vehiculo.codigo,
                        vehiculo.placa,
                        vehiculo.tipo_vehiculo,
                        vehiculo.fecha_inicio.strftime('%Y-%m-%d %H:%M:%S'),
                        vehiculo.fecha_fin.strftime('%Y-%m-%d %H:%M:%S'),
                        vehiculo.numero_entregas,
                        str(vehiculo.facturacion),
                        vehiculo.observacion or '',
                        vehiculo.cliente,
                        'Sí' if vehiculo.validado else 'No'
                    ])
                
                return response


@login_required
def api_real_time_stats(request):
    """API para estadísticas en tiempo real"""
    stats = calculate_real_time_stats(Vehiculo.objects.all())
    return JsonResponse(stats)


@login_required
def api_check_updates(request):
    """API para verificar actualizaciones"""
    last_check = request.session.get('last_check', timezone.now() - timedelta(minutes=5))
    has_updates = Vehiculo.objects.filter(
        updated_at__gt=last_check
    ).exists()
    
    request.session['last_check'] = timezone.now().isoformat()
    
    return JsonResponse({
        'hasUpdates': has_updates,
        'lastCheck': last_check.isoformat() if last_check else None,
        'currentTime': timezone.now().isoformat()
    })


@login_required
def api_vehicle_details(request, vehicle_id):
    """API para detalles de vehículo específico"""
    try:
        vehicle = Vehiculo.objects.get(id=vehicle_id)
        return JsonResponse({
            'success': True,
            'vehicle': {
                'id': vehicle.id,
                'codigo': vehicle.codigo,
                'placa': vehicle.placa,
                'tipo_vehiculo': vehicle.tipo_vehiculo,
                'fecha_inicio': vehicle.fecha_inicio.isoformat(),
                'fecha_fin': vehicle.fecha_fin.isoformat(),
                'numero_entregas': vehicle.numero_entregas,
                'facturacion': str(vehicle.facturacion),
                'observacion': vehicle.observacion,
                'cliente': vehicle.cliente,
                'validado': vehicle.validado,
                'created_at': vehicle.created_at.isoformat() if hasattr(vehicle, 'created_at') else None,
                'updated_at': vehicle.updated_at.isoformat() if hasattr(vehicle, 'updated_at') else None,
            }
        })
    except Vehiculo.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Vehículo no encontrado'
        })


@login_required
def api_bulk_validation(request):
    """API para validación masiva"""
    if request.method == 'POST':
        vehicle_ids = request.POST.getlist('vehicle_ids[]')
        action = request.POST.get('action')  # 'validate' or 'invalidate'
        
        try:
            vehicles = Vehiculo.objects.filter(id__in=vehicle_ids)
            updated_count = 0
            
            for vehicle in vehicles:
                if action == 'validate':
                    vehicle.validado = True
                elif action == 'invalidate':
                    vehicle.validado = False
                
                vehicle.save()
                updated_count += 1
            
            # Invalidar caché
            cache.delete_pattern(f"vehiculos_*")
            
            return JsonResponse({
                'success': True,
                'message': f'Se {action}ron {updated_count} vehículos exitosamente',
                'updated_count': updated_count
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Error en validación masiva: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Método no permitido'
    })
