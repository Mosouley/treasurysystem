# Generated by Django 4.1.6 on 2024-06-08 06:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0032_alter_position_date_alter_trade_tx_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='position',
            field=models.FloatField(),
        ),
    ]
