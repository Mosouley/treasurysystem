# Generated by Django 4.1.6 on 2024-01-04 12:40

from django.db import migrations, models
import shortuuid.main


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0004_alter_trade_trade_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trade',
            name='trade_id',
            field=models.UUIDField(default=shortuuid.main.ShortUUID.uuid, editable=False, unique=True),
        ),
    ]