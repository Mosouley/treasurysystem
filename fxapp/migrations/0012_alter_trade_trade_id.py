# Generated by Django 4.1.6 on 2024-01-04 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0011_alter_trade_date_created_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.CharField(default='18855939868728970357838789056758150706', editable=False, max_length=22, unique=True),
        ),
    ]
