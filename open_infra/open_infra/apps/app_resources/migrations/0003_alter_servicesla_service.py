# Generated by Django 3.2.18 on 2023-05-23 02:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_resources', '0002_auto_20230427_1528'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesla',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app_resources.serviceinfo'),
        ),
    ]
