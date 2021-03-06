# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-07-10 15:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0019_withdrawal_address'),
    ]

    operations = [
        migrations.CreateModel(
            name='WatchedAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=610)),
                ('balance_service', models.CharField(choices=[('BCI', 'BlockChain_Info')], max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='WatchedAddressBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now=True)),
                ('balance', models.DecimalField(blank=True, decimal_places=10, max_digits=26, null=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='charts.WatchedAddress')),
            ],
        ),
    ]
