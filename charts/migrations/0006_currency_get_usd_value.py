# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-19 20:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0005_auto_20170619_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='get_usd_value',
            field=models.BooleanField(default=False),
        ),
    ]
