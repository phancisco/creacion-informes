from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0003_componente_informe_autor_alter_informe_inspector_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitudcambio',
            name='informe',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='solicitudes', to='admin_panel.informe'),
        ),
    ]
