# Generated by Django 4.1.6 on 2024-06-01 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0031_position_position'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='trade',
            name='tx_date',
            field=models.DateField(auto_now=True),
        ),
    ]