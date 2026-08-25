# Generated manually to persist educational presentation metadata.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={
                'ordering': ['name'],
                'verbose_name': 'cliente',
                'verbose_name_plural': 'clientes',
            },
        ),
        migrations.AlterModelOptions(
            name='ticket',
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'ticket',
                'verbose_name_plural': 'tickets',
            },
        ),
    ]
