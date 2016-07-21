# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-20 04:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('mugspot', '0013_auto_20160707_1209'),
    ]

    operations = [
        migrations.CreateModel(
            name='LiveUpdate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=True)),
                ('date_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('place', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='mugspot.MugSpot')),
                ('pos_obj', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='mugspot.Position')),
            ],
        ),
    ]