# Generated by Django 4.1.6 on 2024-01-04 07:28

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0002_alter_trade_trade_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trade',
            name='deal_pnl',
        ),
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.UUIDField(default=uuid.UUID('13389910-7b5c-4f6d-8f58-0b9d0136b8d9')),
        ),
    ]
