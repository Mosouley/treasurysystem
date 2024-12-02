# Generated by Django 5.1.3 on 2024-11-30 12:33

import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0042_rename_intraday_position_position_intraday_pos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ccy',
            options={'verbose_name': 'Currency', 'verbose_name_plural': 'Currencies'},
        ),
        migrations.AlterModelOptions(
            name='systemdailyrates',
            options={'verbose_name_plural': 'Reevaluation Rates'},
        ),
        migrations.RemoveField(
            model_name='systemdailyrates',
            name='rateLcy',
        ),
        migrations.AddField(
            model_name='systemdailyrates',
            name='exchange_rate',
            field=models.DecimalField(decimal_places=4, default=1.0, max_digits=10, validators=[django.core.validators.MinValueValidator(0.0)]),
        ),
        migrations.AlterField(
            model_name='ccy',
            name='code',
            field=models.CharField(max_length=3, unique=True),
        ),
        migrations.AlterField(
            model_name='systemdailyrates',
            name='date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
