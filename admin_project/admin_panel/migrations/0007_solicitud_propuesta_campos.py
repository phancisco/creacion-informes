from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0006_remove_informe_estado_fecha_liberacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudcambio',
            name='propuesta_campos',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
