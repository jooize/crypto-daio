# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-04 12:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('daio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chain',
            name='rcp_user',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chain',
            name='rpc_host',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='chain',
            name='rpc_password',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='chain',
            name='rpc_port',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='chain',
            name='name',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]