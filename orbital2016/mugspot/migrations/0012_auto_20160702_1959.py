# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-02 11:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mugspot', '0011_auto_20160702_1717'),
    ]

    operations = [
        migrations.AddField(
            model_name='person',
            name='faculty',
            field=models.CharField(default=None, max_length=200),
        ),
        migrations.AlterField(
            model_name='person',
            name='friends',
            field=models.ManyToManyField(blank=True, default=None, related_name='_person_friends_+', to='mugspot.Person'),
        ),
    ]
