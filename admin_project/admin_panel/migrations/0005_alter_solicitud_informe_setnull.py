from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0004_solicitud_informe_fk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitudcambio',
            name='informe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='solicitudes', to='admin_panel.informe'),
        ),
    ]
