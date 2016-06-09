# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-08 16:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mugspot', '0005_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='friends',
            field=models.ManyToManyField(blank=True, null=True, related_name='_person_friends_+', to='mugspot.Person'),
        ),
    ]