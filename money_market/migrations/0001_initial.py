# Generated by Django 5.1.3 on 2024-12-01 09:16

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Counterparty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('short_name', models.CharField(max_length=10, unique=True)),
                ('description', models.TextField(default='Full name counterparty')),
                ('category', models.CharField(choices=[('non-group', 'NON-GROUP'), ('group', 'GROUP')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='LimitType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_name', models.CharField(max_length=10, unique=True)),
                ('full_name', models.TextField(default='Full name of the limit')),
                ('category', models.CharField(choices=[('balance-sheet', 'BALANCE SHEET'), ('off-balance-sheet', 'OFF BALANCE SHEET')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Approvals',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_type', models.CharField(max_length=10, verbose_name=[('annual', 'ANNUAL REVIEW'), ('interim', 'INTERIM REVIEW'), ('initial', 'INITIAL REVIEW'), ('exception', 'EXCEPTION APPROVAL')])),
                ('document', models.FileField(upload_to='approval_documents/')),
                ('exception_amount', models.FloatField()),
                ('approval_date', models.DateField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_market.counterparty')),
            ],
        ),
        migrations.CreateModel(
            name='Limits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('limit_amount', models.FloatField()),
                ('limit_approval_date', models.DateField()),
                ('limit_maturity', models.DateField()),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_market.counterparty')),
                ('limit_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_market.limittype')),
            ],
        ),
        migrations.CreateModel(
            name='LimitException',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exception_amount', models.FloatField()),
                ('exception_date', models.DateField(default=django.utils.timezone.now)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_market.counterparty')),
                ('limit_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_market.limittype')),
            ],
        ),
        migrations.CreateModel(
            name='Exposures',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exposure_amount', models.FloatField()),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('counterparty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_market.counterparty')),
                ('limit_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='money_market.limittype')),
            ],
        ),
    ]
