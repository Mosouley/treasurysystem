# Generated by Django 4.1.6 on 2024-01-05 17:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0016_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default=6943, max_length=100, unique=True),
        ),
    ]
