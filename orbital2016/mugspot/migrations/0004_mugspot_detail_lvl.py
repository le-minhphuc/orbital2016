# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-26 06:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mugspot', '0003_auto_20160526_1425'),
    ]

    operations = [
        migrations.AddField(
            model_name='mugspot',
            name='detail_lvl',
            field=models.IntegerField(default=0),
        ),
    ]
