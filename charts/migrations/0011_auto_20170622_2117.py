# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-22 21:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('charts', '0010_auto_20170622_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='currencyvalue',
            name='date_time',
            field=models.DateTimeField(unique=True),
        ),
    ]
