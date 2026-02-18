# Gestión de Vehículos - Django + Power BI

## Descripción

Aplicación web Django para la gestión de viajes de vehículos con funcionalidades de filtrado, validación y exportación de datos para análisis en Power BI.

## Características

### Backend (Django)
- **Modelo de Vehículo** con campos: código, placa, tipo_vehículo, fechas, entregas, facturación, observación, cliente, validado
- **Sistema de autenticación** de usuarios Django
- **Generación automática** de 50 registros de prueba
- **Filtros avanzados**: por placa, rango de fechas, estado de validación
- **Validación AJAX** de registros sin recargar página
- **Exportación** a CSV y Excel con datos filtrados

### Frontend (HTML + CSS + JavaScript)
- **Diseño moderno y responsivo** con gradientes y sombras
- **Interfaz amigable** con estadísticas en tiempo real
- **Tabla ordenada** por fecha_inicio (descendente)
- **Botones de validación** con feedback visual
- **Filtros dinámicos** con aplicación instantánea
- **Badges de color** para tipos de vehículo y estados

## Requisitos

- Python 3.8+
- Django 4.2.7
- pandas 2.1.3
- openpyxl 3.1.2

## Instalación y Configuración

### 1. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar base de datos
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Crear superusuario
```bash
python set_password.py
```

### 4. Generar datos de prueba
```bash
python generar_datos.py
```

### 5. Iniciar servidor
```bash
python manage.py runserver
```

### 6. Acceder a la aplicación
- **URL**: `http://localhost:8000`
- **Usuario**: `admin`
- **Contraseña**: `admin123`

## Uso de la Aplicación

### Login
1. Ingresar con las credenciales proporcionadas
2. El sistema redirige automáticamente al panel principal

### Panel Principal
- **Estadísticas**: Muestra total de vehículos, filtrados y estado
- **Filtros**: Aplicar búsqueda por placa, fechas o validación
- **Tabla**: Lista completa de vehículos con colores diferenciados
- **Validación**: Click en botones para marcar/desmarcar validación
- **Exportación**: Descargar datos filtrados en Excel o CSV

### Funcionalidades AJAX
- La validación se realiza sin recargar la página
- Feedback visual con mensajes de éxito/error
- Actualización automática de la interfaz

## Estructura del Proyecto

```
gestion_vehiculos/
├── gestion_vehiculos/          # Configuración principal
│   ├── settings.py            # Configuración Django
│   └── urls.py               # URLs principales
├── vehiculos/                 # Aplicación principal
│   ├── models.py             # Modelo Vehiculo
│   ├── views.py              # Vistas y lógica
│   ├── urls.py               # URLs de la app
│   └── templates/vehiculos/  # Plantillas HTML
│       ├── login.html        # Formulario de login
│       └── principal.html    # Panel principal
├── generar_datos.py           # Script para datos de prueba
├── requirements.txt           # Dependencias Python
└── README.md                 # Este archivo
```

## Datos de Prueba

El script `generar_datos.py` crea automáticamente:
- **50 registros** de vehículos
- **Distribución**: 15 Turbo, 12 Sencillo, 23 Eléctrico
- **Fechas**: Distribuidas en el último mes
- **Validación**: ~50% validados aleatoriamente
- **Facturación**: Entre $50,000 y $500,000

## Exportación de Datos

### Formatos Disponibles
1. **Excel (.xlsx)**: Con formato optimizado para Power BI
2. **CSV (.csv)**: Formato plano compatible

### Campos Exportados
- Código, Placa, Tipo Vehículo
- Fecha Inicio, Fecha Fin
- Número Entregas, Facturación
- Observación, Cliente, Validado

## Power BI Integration

### Pasos para Dashboard
1. **Exportar datos** desde la aplicación (formato Excel recomendado)
2. **Abrir Power BI Desktop**
3. **Cargar datos** desde el archivo exportado
4. **Crear visualizaciones**:
   - Gráfico de barras: Vehículos por día (fecha_inicio)
   - Tarjeta: Total entregas
   - Tarjeta: Suma facturación
   - Filtros: Por validación y fecha

### Métricas Sugeridas
- **KPIs**: Total vehículos, entregas, facturación
- **Tendencias**: Vehículos por día/semana
- **Distribución**: Por tipo de vehículo
- **Validación**: Porcentaje de registros validados

## Consideraciones Técnicas

### Optimización
- **Consultas eficientes** con Django ORM
- **Filtros en base de datos** (no en memoria)
- **Paginación** implementada para grandes volúmenes
- **AJAX asíncrono** para mejor UX

### Seguridad
- **Autenticación Django** con decoradores @login_required
- **Protección CSRF** en todas las peticiones POST
- **Validación de datos** en backend y frontend

### Estilo y UX
- **Design moderno** con gradientes y sombras
- **Responsive design** para móviles y tablets
- **Feedback visual** inmediato en acciones
- **Colores intuitivos** para estados y tipos

## Capturas de Pantalla

*(Incluir capturas del sistema funcionando)*

1. **Login**: Interfaz de acceso elegante
2. **Panel Principal**: Tabla con filtros y estadísticas
3. **Filtros Aplicados**: Búsqueda por placa y fechas
4. **Validación AJAX**: Acción sin recargar página
5. **Exportación**: Descarga de datos en Excel
6. **Power BI**: Dashboard con visualizaciones

## Comandos para Ejecutar el Proyecto

### **Instalación y Ejecución Completa**
```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Configurar base de datos
python manage.py makemigrations
python manage.py migrate

# 3. Crear superusuario
python set_password.py

# 4. Generar datos de prueba
python generar_datos.py

# 5. Iniciar servidor
python manage.py runserver
```

### **Acceso Rápido**
- **URL**: http://localhost:8000
- **Usuario**: admin
- **Contraseña**: admin123

### **Comandos de Mantenimiento**
```bash
# Recrear datos de prueba
python generar_datos.py

# Reiniciar servidor
python manage.py runserver

# Crear superusuario adicional
python manage.py createsuperuser

# Acceder a shell Django
python manage.py shell
```

### Troubleshooting
- **Error de login**: Verificar credenciales admin/admin123
- **Datos vacíos**: Ejecutar script generar_datos.py
- **Exportación fallida**: Revisar permisos de carpeta

---

**Desarrollado para prueba técnica Django + Power BI**
*Versión 1.0 - Febrero 2026*
