# Generated by Django 4.2.15 on 2024-10-12 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fxapp', '0034_alter_segment_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='cif',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
