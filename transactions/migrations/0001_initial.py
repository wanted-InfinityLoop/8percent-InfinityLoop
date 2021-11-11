# Generated by Django 3.2.9 on 2021-11-11 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32)),
            ],
            options={
                'db_table': 'banks',
            },
        ),
        migrations.CreateModel(
            name='Deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdrawal_account', models.CharField(max_length=32)),
                ('deposit_account', models.CharField(max_length=32, unique=True)),
                ('balance', models.PositiveBigIntegerField(default=0)),
            ],
            options={
                'db_table': 'deposit',
            },
        ),
        migrations.CreateModel(
            name='TransactionType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
            ],
            options={
                'db_table': 'transaction_types',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('information', models.CharField(max_length=64)),
                ('amounts', models.PositiveIntegerField()),
                ('balance', models.PositiveBigIntegerField()),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='transactions.transactiontype')),
            ],
            options={
                'db_table': 'transactions',
            },
        ),
    ]
