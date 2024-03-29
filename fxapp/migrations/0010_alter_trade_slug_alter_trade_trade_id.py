# Generated by Django 4.1.6 on 2024-01-04 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0009_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.UUIDField(default=1704389236, editable=False, unique=True),
        ),
    ]
