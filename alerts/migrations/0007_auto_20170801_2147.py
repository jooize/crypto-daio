# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 21:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0006_auto_20170801_2007'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alert',
            old_name='providers',
            new_name='connectors',
        ),
    ]
