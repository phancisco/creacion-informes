from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0005_alter_solicitud_informe_setnull'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='informe',
            name='fecha_liberacion'
        ),
        migrations.RemoveField(
            model_name='informe',
            name='estado'
        ),
    ]
