# Generated by Django 3.0.6 on 2020-05-07 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0002_auto_20200507_0152'),
    ]

    operations = [
        migrations.RenameField(
            model_name='conta',
            old_name='dia_vendimento',
            new_name='dia_vencimento',
        ),
    ]
