# Generated manually for full stack fields

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('vehiculos', '0002_auto_20260217_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiculo',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='usuario_creacion',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='vehiculos_creados',
                to='auth.user'
            ),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='usuario_modificacion',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='vehiculos_modificados',
                to='auth.user'
            ),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='prioridad',
            field=models.IntegerField(
                choices=[(1, 'Baja'), (2, 'Media'), (3, 'Alta')],
                default=1,
                help_text='Prioridad del vehículo para procesamiento'
            ),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='estado',
            field=models.CharField(
                choices=[('activo', 'Activo'), ('mantenimiento', 'En Mantenimiento'), ('inactivo', 'Inactivo')],
                default='activo',
                help_text='Estado actual del vehículo',
                max_length=20
            ),
        ),
        migrations.AddField(
            model_name='vehiculo',
            name='rendimiento',
            field=models.DecimalField(
                decimal_places=2,
                default=0.00,
                help_text='Índice de rendimiento (entregas/hora)',
                max_digits=5
            ),
        ),
    ]
