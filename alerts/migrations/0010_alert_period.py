# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 22:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0009_auto_20170801_2246'),
    ]

    operations = [
        migrations.AddField(
            model_name='alert',
            name='period',
            field=models.DurationField(default=datetime.timedelta(0, 1200)),
        ),
    ]
