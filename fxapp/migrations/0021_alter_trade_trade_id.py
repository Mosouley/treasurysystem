# Generated by Django 4.1.6 on 2024-01-06 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0020_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default='7fe7d16e-c9ee-4630-9da4-f36c7f559cc2', max_length=100, unique=True),
        ),
    ]
