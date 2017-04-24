# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-22 20:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blocks', '0021_auto_20170421_2316'),
    ]

    operations = [
        migrations.RunSQL('SET CONSTRAINTS ALL IMMEDIATE',
                          reverse_sql=migrations.RunSQL.noop),
        migrations.AlterField(
            model_name='transaction',
            name='tx_id',
            field=models.CharField(max_length=610),
        ),
        migrations.AlterField(
            model_name='txoutput',
            name='script_pub_key_asm',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='txoutput',
            name='script_pub_key_hex',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='txoutput',
            name='script_pub_key_req_sig',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='txoutput',
            name='script_pub_key_type',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.RunSQL(migrations.RunSQL.noop,
                          reverse_sql='SET CONSTRAINTS ALL IMMEDIATE'),
    ]