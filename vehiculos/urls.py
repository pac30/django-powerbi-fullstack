from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.principal_view, name='principal'),
    path('toggle-validacion/', views.toggle_validacion, name='toggle_validacion'),
    path('exportar/', views.exportar_datos, name='exportar_datos'),
    # APIs avanzadas para full stack
    path('api/real-time-stats/', views.api_real_time_stats, name='api_real_time_stats'),
    path('api/check-updates/', views.api_check_updates, name='api_check_updates'),
    path('api/vehicle/<int:vehicle_id>/', views.api_vehicle_details, name='api_vehicle_details'),
    path('api/bulk-validation/', views.api_bulk_validation, name='api_bulk_validation'),
]
