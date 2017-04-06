# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-06 01:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tote', '0003_auto_20170405_2111'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='featuredcompetition',
            options={'ordering': ['order']},
        ),
        migrations.AddField(
            model_name='featuredcompetition',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False),
        ),
    ]