# Generated by Django 5.1.3 on 2024-12-01 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money_market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='approvals',
            name='approval_type',
            field=models.CharField(max_length=25, verbose_name=[('annual', 'ANNUAL REVIEW'), ('interim', 'INTERIM REVIEW'), ('initial', 'INITIAL REVIEW'), ('exception', 'EXCEPTION APPROVAL')]),
        ),
        migrations.AlterField(
            model_name='counterparty',
            name='category',
            field=models.CharField(choices=[('non-group', 'NON-GROUP'), ('group', 'GROUP')], max_length=25),
        ),
        migrations.AlterField(
            model_name='counterparty',
            name='name',
            field=models.CharField(max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='limittype',
            name='category',
            field=models.CharField(choices=[('balance-sheet', 'BALANCE SHEET'), ('off-balance-sheet', 'OFF BALANCE SHEET')], max_length=25),
        ),
        migrations.AlterField(
            model_name='limittype',
            name='short_name',
            field=models.CharField(max_length=25, unique=True),
        ),
    ]
