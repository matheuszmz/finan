# Generated by Django 3.0.6 on 2020-05-07 23:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contas', '0003_auto_20200507_0247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recebimento',
            name='conta',
        ),
        migrations.AddField(
            model_name='recebimento',
            name='responsavel',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='contas.Responsavel'),
            preserve_default=False,
        ),
    ]
