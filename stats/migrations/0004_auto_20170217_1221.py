# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-17 12:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20170217_1204'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='flag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_flags', to='stats.StaticURL'),
        ),
        migrations.AlterField(
            model_name='team',
            name='shirt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='team_shirts', to='stats.StaticURL'),
        ),
    ]
