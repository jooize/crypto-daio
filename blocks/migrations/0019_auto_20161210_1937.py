# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-12-10 19:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0018_auto_20161128_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='block',
            name='next_block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next', to='blocks.Block'),
        ),
        migrations.AlterField(
            model_name='block',
            name='previous_block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='previous', to='blocks.Block'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='block',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', related_query_name='transaction', to='blocks.Block'),
        ),
        migrations.AlterField(
            model_name='txinput',
            name='output_transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inout_txs', related_query_name='inout_tx', to='blocks.Transaction'),
        ),
        migrations.AlterField(
            model_name='txinput',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='inputs', related_query_name='input', to='blocks.Transaction'),
        ),
        migrations.AlterField(
            model_name='txoutput',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='outputs', related_query_name='output', to='blocks.Transaction'),
        ),
    ]
