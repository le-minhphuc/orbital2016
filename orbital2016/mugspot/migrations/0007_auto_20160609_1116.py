# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-09 03:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mugspot', '0006_auto_20160609_0002'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='friends',
            field=models.ManyToManyField(blank=True, to='mugspot.Person'),
        ),
    ]
